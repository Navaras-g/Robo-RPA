import os
from robocorp.tasks import task
from robocorp  import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive


@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    os.makedirs("output/receipts", exist_ok=True)
    os.makedirs("output/screenshots", exist_ok=True)

    open_robot_Order_website()
    download_csv_file()
    orders = get_orders()

    for order in orders:
        close_annoying_model()
        fill_the_form(order)
        preview_the_robot()
        submit_order()

        pdf_file = store_receipt_as_pdf(order["Order number"])
        screenshot = screenshot_robot(order["Order number"])
        embed_screenshot_to_receipt(screenshot, pdf_file)

        order_another_robot()

    archive_receipts()


def open_robot_Order_website():
    """opens the order website"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")


def download_csv_file():
    """downloads the order file"""
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", target_file="orders.csv", overwrite=True)


def get_orders():
    """read the csv file into tables and return the result """
    tables = Tables()
    return tables.read_table_from_csv("orders.csv", header=True)


def close_annoying_model():
    """closes the annoying pop up when visiting the order website"""
    page = browser.page()
    page.click("button:has-text('OK')")


def fill_the_form(order):
    """fill the order form to order the robot"""
    page = browser.page()

    page.select_option("#head", str(order["Head"]))
    page.click(f"#id-body-{order['Body']}")
    page.fill("input[placeholder='Enter the part number for the legs']", str(order["Legs"]))
    page.fill("#address", str(order["Address"]))


def preview_the_robot():
    """preview to see how the robot looks like"""
    page = browser.page()
    page.click("#preview")


def submit_order():
    """submit the user order and retries if there is an error"""
    page = browser.page()

    while True:
        page.click("#order")
        receipt = page.query_selector("#receipt")

        if receipt:
            break


def order_another_robot():
    """orders another robot for the next user"""

    page = browser.page()
    page.click("#order-another")


def store_receipt_as_pdf(order_number):
    """stores the order receipt as pdf"""
    page = browser.page()

    receipt_html = page.locator("#receipt").inner_html()

    pdf = PDF()
    pdf_path = f"output/receipts/order_{order_number}.pdf"
    pdf.html_to_pdf(receipt_html, pdf_path)
    return pdf_path


def screenshot_robot(order_number):
    """take the screenshot of the page"""
    page = browser.page()

    screenshot_path = f"output/screenshots/robot_{order_number}.png"
    page.locator("#robot-preview-image").screenshot(path=screenshot_path)
    return screenshot_path


def embed_screenshot_to_receipt(screenshot, pdf_file):
    """embeds the robot screenshot to the pdf file"""
    pdf = PDF()

    pdf.add_watermark_image_to_pdf(image_path=screenshot, source_path= pdf_file, output_path= pdf_file)


def archive_receipts():
    """archives all PDF receipts into a ZIP file"""
    archive = Archive()
    archive.archive_folder_with_zip("output/receipts", "output/receipts.zip")