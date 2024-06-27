import pytest

user_data = [
    ("standard_user", "secret_sauce", "Larry", "David", "1101"),
    ("locked_out_user", "secret_sauce", "John", "Smith", "2202"),
    ("problem_user", "secret_sauce", "Emily", "Johnson", "3303"),
    ("performance_glitch_user", "secret_sauce", "Michael", "Williams", "4404"),
    ("error_user", "secret_sauce", "Jessica", "Brown", "5505"),
    ("visual_user", "secret_sauce", "Daniel", "Jones", "6606")
]


@pytest.mark.usefixtures("setup")
class TestE2E:

    @pytest.mark.parametrize("username, password, firstname, lastname, zipcode", user_data)
    def test_checkout_flow(self, username, password, firstname, lastname, zipcode):
        # initialize pages
        login_page = self.page_manager.get_login_page()
        product_page = self.page_manager.get_product_page()
        cart_page = self.page_manager.get_cart_page()
        checkout_form_page = self.page_manager.get_checkout_form_page()
        checkout_overview_page = self.page_manager.get_checkout_overview_page()
        checkout_complete_page = self.page_manager.get_checkout_complete_page()

        # collecting errors for soft assertions
        errors = []

        # login
        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.click_login_button()
        assert login_page.check_for_error() is None, "Login failed."

        # pick items, go to cart
        product_page.sort_price_low_high()
        product_page.add_onesie()
        product_page.add_bike()
        products = product_page.get_items()
        product_page.go_to_cart()

        # verify products in cart
        cart_items = cart_page.get_items()
        for product, item in zip(products, cart_items):
            if product[0] != item[0]:
                errors.append(f"Product {product[0]} != cart item: {item[0]} ")
            if product[1] != item[1]:
                errors.append(f"Product price {product[1]} != cart item price: {item[1]} ")
        cart_page.go_to_checkout()

        # fill-out checkout form
        checkout_form_page.enter_firstname(firstname)
        checkout_form_page.enter_lastname(lastname)
        checkout_form_page.enter_zip(zipcode)
        checkout_form_page.go_continue()

        # verify order details
        # >validate prices
        checkout_overview_page.go_finish()

        # verify order complete
        if "Thank you for your order!" != checkout_complete_page.get_thankyou():
            errors.append("Order not completed")

        assert not errors, f"Errors: {errors}"
