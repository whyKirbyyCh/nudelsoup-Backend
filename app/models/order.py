from typing import Dict


class Order:
    """
    Class representing an order.
    """

    def __init__(self, services: Dict[str, bool], company_info: Dict[str, Dict[str, str]], product_info: Dict[str, Dict[str, str]], SSCOP: bool = False, CPOP: bool = False, SSPOP: bool = False, PPSOP: bool = False) -> None:
        """
        Initializes the class with the company info and services.

        Args:
            company_info (Dict[str, Dict[str, str]]): The company information.
            product_info (Dict[str, Dict[str, str]]): The product information.
            SSCOP (str): The Site Specific Company Optimised Prompt.
            CPOP (str): The Company Profile Optimised Prompt.
            SSPOP (str): The Site Specific Product Optimised Prompt.
            PPSOP (str): The Product Profile Specific Optimised Prompt.

        Raises:
            ValueError: If the company info or product info is empty.
        """
        if not services:
            raise ValueError("services must not be empty")

        if not company_info:
            raise ValueError("company_info must not be empty")

        if not product_info:
            raise ValueError("product_info must not be empty")

        self.services: Dict[str, bool] = services
        self.company_info: Dict[str, Dict[str, str]] = company_info
        self.product_info: Dict[str, Dict[str, str]] = product_info

        if SSCOP:
            self.SSCOP: Dict[str, str] = self._collect_SSCOP(company_info)
        else:
            self.SSCOP: Dict[str, str] = {"all": "No optimisations are wanted for this specific Site and this specific Company Profile."}

        if CPOP:
            self.CPOP: Dict[str, str] = self._collect_CPOP(company_info)
        else:
            self.CPOP: Dict[str, str] = {"all": "No optimisations are wanted for this specific Site and this specific Company Profile."}

        if SSPOP:
            self.SSPOP: Dict[str, str] = self._collect_SSPOP(product_info)
        else:
            self.SSPOP: Dict[str, str] = {"all": "No optimisations are wanted for this specific Site and this specific Company Profile."}

        if PPSOP:
            self.PPSOP: Dict[str, str] = self._collect_PPSOP(product_info)
        else:
            self.PPSOP: Dict[str, str] = {"all": "No optimisations are wanted for this specific Site and this specific Company Profile."}

        self.order_details: Dict[str, Dict[str, Dict[str, str]]] = {"system": {"SSCOP": self.SSCOP, "CPOP": self.CPOP}, "user": {"SSPOP": self.SSPOP, "PPSOP": self.PPSOP}}

    def _collect_SSCOP(self, company_info: Dict[str, Dict[str, str]]) -> Dict[str, str]:
        """
        Collects the Site Specific Company Optimised Prompt.

        Args:
            company_info (Dict[str, Dict[str, str]]): The company information.

        Returns:
            str: The Site Specific Company Optimised Prompt.
        """
        SSCOP: Dict[str, str] = {}

        for service, value in self.services.items():
            if value:
                SSCOP[service] = "No optimisation has been found for this specific Site and this specific Company Profile."
            else:
                SSCOP[service] = "No optimisation is wanted for this specific Site and this specific Company Profile."

        return SSCOP

    def _collect_CPOP(self, company_info: Dict[str, Dict[str, str]]) -> Dict[str, str]:
        """
        Collects the Company Profile Optimised Prompt.

        Args:
            company_info (Dict[str, Dict[str, str]]): The company information.

        Returns:
            str: The Company Profile Optimised Prompt.
        """
        CPOP: Dict[str, str] = {}

        for service, value in self.services.items():
            if value:
                CPOP[service] = "No optimisation has been found for this specific Site and this specific Company Profile."
            else:
                CPOP[service] = "No optimisation is wanted for this specific Site and this specific Company Profile."

        return CPOP

    def _collect_SSPOP(self, product_info: Dict[str, Dict[str, str]]) -> Dict[str, str]:
        """
        Collects the Site Specific Product Optimised Prompt.

        Args:
            product_info (Dict[str, Dict[str, str]]): The product information.

        Returns:
            str: The Site Specific Product Optimised Prompt.
        """
        SSPOP: Dict[str, str] = {}

        for service, value in self.services.items():
            if value:
                SSPOP[service] = "No optimisation has been found for this specific Site and this specific Company Profile."
            else:
                SSPOP[service] = "No optimisation is wanted for this specific Site and this specific Company Profile."

        return SSPOP

    def _collect_PPSOP(self, product_info: Dict[str, Dict[str, str]]) -> Dict[str, str]:
        """
        Collects the Product Profile Specific Optimised Prompt.

        Args:
            product_info (Dict[str, Dict[str, str]]): The product information.

        Returns:
            str: The Product Profile Specific Optimised Prompt.
        """
        PPSOP: Dict[str, str] = {}

        for service, value in self.services.items():
            if value:
                PPSOP[
                    service] = "No optimisation has been found for this specific Site and this specific Company Profile."
            else:
                PPSOP[service] = "No optimisation is wanted for this specific Site and this specific Company Profile."

        return PPSOP
