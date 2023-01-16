"""
A python program that will take all of the orders placed for all of the stores each week,
and summarize the information into an easy to read table that tells the store owners
how many drivers will be needed to deliver all of the packages for that week
Author: Muhammad Safwan Hossain
"""


class Deliveries:
    """
    This class initializes a delivery service with different methods calculating the
    order information, packaging and displaying invoice and the summary
    """

    def __init__(self):
        self.product = {}
        self.zones = {}
        self.orders = {}
        self.zone_code_dict = {}
        self.continue_delivery = True
        self.driver_package_count = 10
        self.package_delivery_charge = 12

    def order_file(self):
        # read the text file for order

        file_name = open('orders.txt', 'r')
        order_file = file_name.read()
        order_line = order_file.split("\n")

        for line in order_line:
            date, buyer, address, product_id, items_bought = line.split('%')
            # appending the data to a dict
            self.orders[address] = self.orders.get(address, [])
            self.orders[address].append({'date': date, 'name': buyer,
                                         'product_id': product_id, 'items_bought': int(items_bought)})
        file_name.close()

    def product_file(self):
        # read the text file for products

        file_name = open('products.txt', 'r')
        product_file = file_name.read()
        product_line = product_file.split("\n")

        for line in product_line:
            product_id, name, product_price = line.split(";")

            self.product[product_id] = {'product_name': name,
                                        'price': int(product_price)}
        file_name.close()

    def zone_file(self):
        # read the text file for zones

        file_name = open('zones.txt', 'r')
        zone_file = file_name.read()
        zone_line = zone_file.split("\n")

        for line in zone_line:
            # splitting the zones into small areas
            zone, zone_codes = line.split('#')
            zone_codes = zone_codes.split(',')

            self.zones[zone] = zone_codes

            for each_code in zone_codes:
                self.zone_code_dict[each_code] = zone
        file_name.close()

    def continue_deli(self):
        # start the program

        # reading all the files
        self.product_file()
        self.order_file()
        self.zone_file()

        # checking if the program is still or not
        while self.continue_delivery:
            self.display_prompt()

            # asking user for an input
            user_input = input("> ")

            # checking for correct input
            while not user_input.isdigit() or not 0 <= int(user_input) <= 3:
                print("Sorry, invalid entry. Please enter a choice from 1 to 3.")
                user_input = input("> ")

            # starting a program according to the input
            if int(user_input) == 1:
                self.prompt1()
            elif int(user_input) == 2:
                self.prompt2()
            else:
                self.prompt3()

    def display_prompt(self):
        # displaying the first menu option of the program
        title = "Welcome to the Small Business Delivery Program"
        row_padding = len(title) * "*"
        header = row_padding + '\n' + title + '\n' + row_padding + '\n'

        first = "What would you like to do?\n"
        second = "1. Display DELIVERY SUMMARY TABLE for this week\n"
        third = "2. Display and save DELIVERY ORDER for specific address\n"
        fourth = "3. Quit"

        menu = first + second + third + fourth

        print(header + menu)

    def prompt1(self):
        # displaying the option 1 for prompt 1

        table, display_info = self.driver_calculation()

        # paddings, bars and headers
        headers = ["Delivery Zone", "Deliveries", " Drivers "]
        columns = ["-" * 15, "-" * 12, "-" * 11]
        dividers = "+{}+{}+{}+".format(columns[0], columns[1], columns[2])
        padding = "|"
        list_of_alignment = ['<', '^', '^']

        # printing the categories and "-"
        print(dividers)
        print("{} {} {} {} {} {} {}".format(padding, headers[0], padding, headers[1], padding, headers[2], padding))
        print(dividers)

        # printing each element within the table
        for segment in table:
            print("{} ".format(padding), end="")
            print(f" {padding} ".join(f"{deli:{list_of_alignment[loc]}{len(columns[loc]) - 2}}"
                                      for loc, deli in enumerate(segment)), end="")
            print(" {}".format(padding))

        print(dividers)

        # printing total driver information
        driver_number, cost_total, percent = display_info

        final_options = ['Total drivers needed', 'Total delivery cost', 'Delivery cost/purchases']

        options_output = {final_options[0]: driver_number, final_options[1]: '$ ' + "{:.2f}".format(cost_total),
                          final_options[2]: "{:.1f}%".format(percent)}

        for option in final_options:
            print("{} ".format(padding), end="")
            print("{:<27}".format(option), end="")
            print("{:>11}".format(options_output[option]), end="")
            print(" {}".format(padding))

        print("+----------------------------------------+\n")

    def prompt2(self):
        # displaying the option 2 for prompt 2

        # asking for an address
        user_input = input("Address: ")

        # check if the address is valid or not
        if not self.orders.get(user_input, False):
            print("Invalid address.\n")

            return

        # display option
        header_items = ["Date", "Item", "Price"]
        columns = ['------ ', '-------------------------- ', '---------']
        header_pads = "=" * 45
        delivery_order = ''
        price_count = 0.0
        deli_print = len(header_pads) - len("Delivery for:")

        # checking if the address if within 30 spaces
        if self.pos_calculation(user_input, 30):
            delivery_order = ("Delivery for:" + f"{user_input:>{deli_print}}") + '\n'
            delivery_order = delivery_order + header_pads + '\n'
            delivery_order = delivery_order + (
                " ".join(f"{header:<{len(columns[pos])}}" for pos, header in enumerate(header_items))) + "\n"
            delivery_order = delivery_order + (" ".join(columns)) + '\n'

        # displaying specific order details
        req_orders = self.order_loc(user_input)
        for order in req_orders:
            date, items_bought, product_name, price = order

            date_output = self.display_dates(date)
            name_output = " " + "{:03} X {:20}".format(items_bought, self.pos_calculation(product_name, 20))
            price_output = "  " + "{:>8.2f}".format(price)
            delivery_order = delivery_order + (" ".join([date_output, name_output, price_output])) + '\n'

            # calculating the total sum
            price_count += float(price)

        # aligning the summation bars and total price
        summation_line = " {:^}".format(columns[-1])
        delivery_order = delivery_order + f'{summation_line:>{len(header_pads)}}' + "\n" + f'{"$":>{len(header_pads) - 8}}  {price_count:>.2f}'

        print(delivery_order + '\n')

        # writing in a text file
        text_file = open("invoice.txt", 'w')
        text_file.write(delivery_order)

    def prompt3(self):
        # displaying the option 3 for prompt 3

        self.continue_delivery = False
        print("Thank you for using the Small Business Delivery Program! Goodbye.")

    def driver_calculation(self):
        # calculating the number of drivers and the overall information for option 1

        cost_of_products = 0
        package_count = {}
        driver_no = 0
        total_packages = 0
        option1_summary = []

        # calculating total cost
        for address in self.orders:
            zone = self.zone_code_dict[self.calculate_address(address)]

            # adding 1 as for 1 package
            package_count[zone] = package_count.get(zone, 0) + 1

            calculations = self.cost_of_items(self.orders[address])
            cost_of_products += calculations

        # calculating the number of drivers per zone
        for zone in package_count:
            each_package = package_count[zone]
            total_packages += each_package

            if each_package % self.driver_package_count == 0:
                drivers = each_package // self.driver_package_count
            else:
                drivers = each_package // self.driver_package_count + 1

            # summing up the number of drivers
            driver_no += drivers

            option1_summary.append((zone, each_package, drivers))

        # sorting the overall summary
        option1_summary.sort()

        # calculating total drivers cost and percentage
        cost_of_delivery = total_packages * self.package_delivery_charge
        percentage = (cost_of_delivery / cost_of_products) * 100

        display_info = driver_no, cost_of_delivery, percentage

        return option1_summary, display_info

    def cost_of_items(self, orders):
        # calculating the total amount of cost
        total_amount = 0

        for order in orders:
            product_id = order['product_id']
            items_bought = order['items_bought']

            price_per_order = self.product[product_id]['price']
            cost_of_order = (price_per_order / 100) * items_bought
            total_amount += cost_of_order

        return total_amount

    def calculate_address(self, address):
        # calculating the position of the address

        # postal codes for each zone is from the 7th position to last 4th position
        code = address[-7:]
        exact_address = code[:3]
        return exact_address

    def display_dates(self, dates):
        # changing the output of the dates

        months = {1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN", 7: "JUL", 8: "AUG", 9: "SEP", 0: "OCT",
                  11: "NOV", 12: "DEC"}

        year, month, date = dates.split('-')
        formatted_date = "{} {}".format(months[int(month)], date)

        return formatted_date

    def pos_calculation(self, num, len_no):
        # calculating the length position of words and substituting it with "*"
        if len(num) > len_no:
            star = f'{num[:len_no - 1]}*'
        else:
            star = num
        return star

    def order_loc(self, loc):
        # calculation of individual orders for option2
        output_list = []
        order_id = self.orders[loc]

        for per_package in order_id:
            dates = per_package['date']
            items_bought = per_package['items_bought']
            product_no = per_package['product_id']
            price_for_one = self.product[product_no]['price']
            product_name = self.product[product_no]['product_name']

            # calculating the value
            calc_price = (price_for_one / 100) * items_bought
            output_list.append((dates, items_bought, product_name, calc_price))

        return output_list


def main():
    # this is the main function
    deliveries = Deliveries()
    deliveries.continue_deli()


main()
