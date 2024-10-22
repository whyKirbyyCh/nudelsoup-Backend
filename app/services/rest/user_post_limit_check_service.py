from app.db.db_connection import DBConnection
from app.excpetions.rest.user_limits_exception import UserLimitsException
from app.excpetions.db.db_connection_exception import DBConnectionException
from pymongo.collection import Collection
import datetime
from app.config.logger_config import Logger
import traceback
from typing import Dict, Optional
from bson import ObjectId


class UserPostLimitCheckService:
    """Class checks if a user's limit has been reached."""

    logger = Logger.get_logger()
    _db_connection: DBConnection = None

    @classmethod
    def initialize_db_connection(cls):
        """Initializes the database connection."""
        if cls._db_connection is None:
            try:
                cls._db_connection = DBConnection()
                cls.logger.info("Database connection initialized.")
            except Exception as e:
                cls.logger.error(f"Failed to initialize database connection: {e}")
                raise DBConnectionException("Could not connect to the database. 1")

    @classmethod
    def close_db_connection(cls):
        """Closes the database connection."""
        if cls._db_connection is not None:
            cls._db_connection.close_connection()
            cls._db_connection = None
            cls.logger.info("Database connection closed.")

    @classmethod
    def check_user_limit(cls, user_id: str) -> bool:
        """
        Checks if the user limit has been reached.

        Returns:
            bool: True if the user limit has been reached, False otherwise.

        Raises:
            DBConnectionException: If the database connection fails.
            UserLimitsException: If the user limit has been reached.
        """
        cls.initialize_db_connection()

        try:
            collection: Collection = cls._db_connection.get_collection(collection_name="activity")
            user_activities: Optional[Dict] = collection.find_one({"userId": user_id})

            if user_activities is None:
                user_activities = cls._initialize_limit(user_id)
                try:
                    collection.insert_one(user_activities)
                except Exception:
                    raise DBConnectionException("Failed to insert new user activities into the database.")
            else:
                user_activities = dict(user_activities)

            check_if_update_needed: bool = cls._check_if_update_needed(
                user_activities["nextRefresh"],
                user_activities["lastRefresh"],
                user_activities["hasBeenRefreshed"]
            )

            if check_if_update_needed:
                user_activities = cls._refresh_limit(user_activities)

            if user_activities["amountLeft"] <= 0:
                raise UserLimitsException("User has reached the limit for this billing period. 1")
            else:
                updated_user_activities: dict = cls._update_limit(user_activities)
                collection.replace_one({"userId": user_id}, updated_user_activities)

                return True

        except DBConnectionException:
            raise DBConnectionException("Could not connect to the database.")

        except UserLimitsException:
            raise UserLimitsException("User has reached the limit for this billing period.")

        except Exception as e:
            cls.logger.error(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
            raise UserLimitsException(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")

        finally:
            cls.close_db_connection()

    @classmethod
    def _check_if_update_needed(cls, next_refresh: str, last_refresh: str, has_been_refreshed: bool) -> bool:
        """
        Checks if the user limit gets refreshed.

        Args:
            next_refresh (str): The next refresh date.
            last_refresh (str): The last refresh date.
            has_been_refreshed (bool): Whether the user limit has been refreshed or not.

        Returns:
            bool: True if the user limit gets refreshed, False otherwise.

        Raises:
            UserLimitsException: If there is something wrong with the user limit.
        """
        next_refresh_date: datetime = datetime.datetime.strptime(next_refresh, "%Y-%m-%d")
        last_refresh_date: datetime = datetime.datetime.strptime(last_refresh, "%Y-%m-%d")

        if next_refresh_date.date() <= datetime.datetime.today().date():
            if last_refresh_date.date() == datetime.datetime.today().date():
                if has_been_refreshed:
                    cls.logger.error("User has refreshed the limit today, but the limit has not been refreshed yet.")
                    raise UserLimitsException("User has refreshed the limit today, but the limit has not been refreshed yet.")
                else:
                    return False

        return True

    @classmethod
    def _initialize_limit(cls, user_id: str) -> Dict:
        """
        Initializes the user limit.

        Args:
            user_id (str): The user id.

        Returns:
            Dict: The initialized user activities.
        """
        limit_per_period: int = cls._get_limit(user_id)
        current_date: str = datetime.datetime.today().strftime("%Y-%m-%d")
        next_refresh: str = (datetime.datetime.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")

        user_activities: Dict = {
            "_id": ObjectId(),
            "userId": user_id,
            "amountLeft": limit_per_period,
            "amountUsed": 0,
            "limitPerPeriod": limit_per_period,
            "nextRefresh": next_refresh,
            "lastRefresh": current_date,
            "hasBeenRefreshed": True,
            "period": "30 days"
        }

        return user_activities

    @classmethod
    def _refresh_limit(cls, user_activities: Dict) -> Dict:
        """
        Refreshes the user limit.

        Args:
            user_activities (Dict): The user activities.

        Returns:
            Dict: The refreshed user activities.
        """
        user_activities["amountLeft"] = user_activities["limitPerPeriod"]
        user_activities["amountUsed"] = 0

        current_date: str = datetime.datetime.today().strftime("%Y-%m-%d")
        next_refresh_date: str = (datetime.datetime.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")

        user_activities["lastRefresh"] = current_date
        user_activities["nextRefresh"] = next_refresh_date
        user_activities["hasBeenRefreshed"] = True

        return user_activities

    @classmethod
    def _update_limit(cls, user_activities: Dict) -> Dict:
        """
        Updates the user limit.

        Args:
            user_activities (Dict): The user activities.

        Returns:
            Dict: The updated user activities.
        """
        if user_activities["amountLeft"] > 0:
            user_activities["amountLeft"] -= 1
            user_activities["amountUsed"] += 1

            if user_activities["hasBeenRefreshed"]:
                user_activities["hasBeenRefreshed"] = False
        else:
            raise UserLimitsException("User has no remaining limits.")

        return user_activities

    @classmethod
    def _get_limit(cls, user_id: str) -> int:
        """
        Gets the user limit.

        Args:
            user_id (str): The user id.

        Returns:
            int: The user limit.
        """
        cls._db_connection.get_collection(collection_name="users")

        try:
            user: Dict = cls._db_connection.get_collection(collection_name="users").find_one({"_id": ObjectId(user_id)})

            if not user:
                cls.logger.error("User not found in DB.")
                raise UserLimitsException("User not found.")

            user_limit: int

            if user["priceId"] == "price_1Q2QBj08drlwCs6aDl3flY9N":  # this is the "DINNER FOR ONE - YEARLY" price
                user_limit = 10 * 12
            elif user["priceId"] == "price_1Q1TW908drlwCs6ax12Ghvy6":  # this is the "DINNER FOR ONE - MONTHLY" price
                user_limit = 10
            elif user["priceId"] == "price_1Q2Q9O08drlwCs6aHJFwQMKc":  # this is the "FAMILY SIZED MEAL - YEARLY" price
                user_limit = 20 * 12
            elif user["priceId"] == "price_1Q1TWT08drlwCs6aGgJQRbuk":  # this is the "FAMILY SIZED MEAL - MONTHLY" price
                user_limit = 20
            elif user["priceId"] == "price_1Q1UEn08drlwCs6aFmwjFxJI":  # this is the "DELUXE PARTY BUFFET - YEARLY" price
                user_limit = 30 * 12
            elif user["priceId"] == "price_1Q1TWi08drlwCs6aJEvcKVCK":  # this is the "DELUXE PARTY BUFFET - MONTHLY" price
                user_limit = 30
            else:
                raise UserLimitsException("User price not found.")

            return user_limit

        except UserLimitsException:
            raise UserLimitsException("User not found.")

        except Exception as e:
            raise UserLimitsException(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
