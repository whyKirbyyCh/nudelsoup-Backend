from typing import Dict


class Order:
    """
    Class representing an order.
    """

    def __init__(self, services: Dict[str, bool], company_info: Dict[str, Dict[str, str]], product_info: Dict[str, Dict[str, str]], sscop: bool = False, cpop: bool = False, sspop: bool = False, ppsop: bool = False) -> None:
        """
        Initializes the class with the company info and services.

        Args:
            company_info (Dict[str, Dict[str, str]]): The company information.
            product_info (Dict[str, Dict[str, str]]): The product information.
            sscop (str): The Site Specific Company Optimised Prompt.
            cpop (str): The Company Profile Optimised Prompt.
            sspop (str): The Site Specific Product Optimised Prompt.
            ppsop (str): The Product Profile Specific Optimised Prompt.

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

        if sscop:
            self.sscop: Dict[str, str] = self._collect_sscop(company_info)
        else:
            self.sscop: Dict[str, str] = {"all": "No optimisations are wanted with regard to the site and the company for this specific Site and this specific Company Profile."}

        if cpop:
            self.cpop: Dict[str, str] = self._collect_cpop(company_info)
        else:
            self.cpop: Dict[str, str] = {"all": "No optimisations are wanted with regard to the company for this specific Site and this specific Company Profile."}

        if sspop:
            self.sspop: Dict[str, str] = self._collect_sspop(product_info)
        else:
            self.sspop: Dict[str, str] = {"all": "No optimisations are wanted with regard to the product and the site for this specific Site and this specific Company Profile."}

        if ppsop:
            self.ppsop: Dict[str, str] = self._collect_ppsop(product_info)
        else:
            self.ppsop: Dict[str, str] = {"all": "No optimisations are wanted with regard to the product for this specific Site and this specific Company Profile."}

        self.order_details: Dict[str, Dict[str, Dict[str, str]]] = {"system": {"sscop": self.sscop, "cpop": self.cpop}, "user": {"sspop": self.sspop, "ppsop": self.ppsop}}

    def _collect_sscop(self, company_info: Dict[str, Dict[str, str]]) -> Dict[str, str]:
        """
        Collects the Site Specific Company Optimised Prompt.

        Args:
            company_info (Dict[str, Dict[str, str]]): The company information.

        Returns:
            str: The Site Specific Company Optimised Prompt.
        """
        sscop: Dict[str, str] = {}

        for service, value in self.services.items():
            if value:
                sscop[service] = "No optimisation has been found with regard to the site and the company for this specific Site and this specific Company Profile."
            else:
                sscop[service] = "No optimisations are wanted with regard to the site and the company for this specific Site and this specific Company Profile."

        return sscop

    def _collect_cpop(self, company_info: Dict[str, Dict[str, str]]) -> Dict[str, str]:
        """
        Collects the Company Profile Optimised Prompt.

        Args:
            company_info (Dict[str, Dict[str, str]]): The company information.

        Returns:
            str: The Company Profile Optimised Prompt.
        """
        cpop: Dict[str, str] = {}

        for service, value in self.services.items():
            if value:
                cpop[service] = "No optimisation has been found with regard to the company for this specific Site and this specific Company Profile."
            else:
                cpop[service] = "No optimisations are wanted with regard to the company for this specific Site and this specific Company Profile."

        return cpop

    def _collect_sspop(self, product_info: Dict[str, Dict[str, str]]) -> Dict[str, str]:
        """
        Collects the Site Specific Product Optimised Prompt.

        Args:
            product_info (Dict[str, Dict[str, str]]): The product information.

        Returns:
            str: The Site Specific Product Optimised Prompt.
        """
        sspop: Dict[str, str] = {}

        for service, value in self.services.items():
            if value:
                sspop[service] = "No optimisation has been found with regard to the product and the site for this specific Site and this specific Company Profile."
            else:
                sspop[service] = "No optimisations are wanted with regard to the product and the site for this specific Site and this specific Company Profile."

        return sspop

    def _collect_ppsop(self, product_info: Dict[str, Dict[str, str]]) -> Dict[str, str]:
        """
        Collects the Product Profile Specific Optimised Prompt.

        Args:
            product_info (Dict[str, Dict[str, str]]): The product information.

        Returns:
            str: The Product Profile Specific Optimised Prompt.
        """
        ppsop: Dict[str, str] = {}

        for service, value in self.services.items():
            if value:
                ppsop[
                    service] = "No optimisation has been found with regard to the product for this specific Site and this specific Company Profile."
            else:
                ppsop[service] = "No optimisations are wanted with regard to the product for this specific Site and this specific Company Profile."

        return ppsop
