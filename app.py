
from flask import Flask
from flask_restful import Api, Resource
from selenium import webdriver

app = Flask(__name__)
api = Api(app)

def check_usdot(usdot:int):
    # Check USDOT in site https://safer.fmcsa.dot.gov/
    browser = webdriver.Chrome('./chromedriver')
    browser.minimize_window()
    try:
        browser.get('https://safer.fmcsa.dot.gov/CompanySnapshot.aspx')
    except Exception as error_string:
        print(error_string)
        return None
    # Enter the USDOT in the field
    input_block = '/html/body/form/p/table/tbody/tr[3]/td/input'
    browser.find_element_by_xpath(input_block).send_keys(usdot)
    # Press the button Search
    search_buttom = '/html/body/form/p/table/tbody/tr[4]/td/input'
    browser.find_element_by_xpath(search_buttom).click()
    # Get parameters
    try:
        entity_type = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[2]/td').text
    except Exception as errors_string:
        print(errors_string)
        return None
    operating_status = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[3]/td[1]').text
    out_of_service_date = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[3]/td[2]').text
    legal_name = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[4]/td').text
    DBA_name = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[5]/td').text
    physical_address = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[6]/td').text
    phone = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[7]/td').text
    mailing_address = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[8]/td').text
    USDOT_number = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[9]/td[1]').text
    state_carrier_ID_number = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[9]/td[2]').text
    MC_MX_FF_number = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[10]/td[1]').text
    power_units = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[11]/td[1]').text
    drivers = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[11]/td[2]').text
    MCS_150_form_date = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[12]/td[1]').text
    MCS_150_mileage_year = browser.find_element_by_xpath('/html/body/p/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center[1]/table/tbody/tr[12]/td[2]').text

    # Create output json
    json_response = {
        "Entity Type" : entity_type,
        "Operating Status" : operating_status,
        "Out of Service Date" : out_of_service_date,
        "Legal Name" : legal_name,
        "DBA Name" : DBA_name,
        "Physical Address" : physical_address,
        "Phone" : phone,
        "Mailing Address" : mailing_address,
        "USDOT Number" : USDOT_number,
        "State Carrier ID Number" : state_carrier_ID_number,
        "MC/MX/FF Number(s)" : MC_MX_FF_number,
        "Power Units" : power_units,
        "Drivers" : drivers,
        "MCS-150 Form Date" : MCS_150_form_date,
        "MCS-150 Mileage (Year)" : MCS_150_mileage_year
    }

    browser.close()
    return json_response

class Requests(Resource):
    def get(self, usdot):
            if usdot is not None:
                return check_usdot(usdot), 200
            else:
                return "usdot not found", 404
#
api.add_resource(Requests, "/check_usdot/<int:usdot>")

if __name__ == '__main__':
    app.run(debug=True)
