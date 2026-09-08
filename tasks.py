from robocorp.tasks import task
from robocorp  import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF


@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    open_robot_Order_website()
    


def open_robot_Order_website():
    """opens the order website"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")


def download_csv_file():
    """downloads the order file"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite= True)


def get_orders():
    """read the csv file into tables that can be looped"""
    tables = Tables()
    tables.read_table_from_csv("order.csv", header=True)


def close_annoying_model():
    """closes the annoying pop up when visiting the order website"""


def fill_the_form():
    """fill the order form to order the robot"""


