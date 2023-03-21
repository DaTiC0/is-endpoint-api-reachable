# Testing the Merchant API is reachable or not
# Author: DaTi_Co

# import the necessary packages
import requests
import pandas as pd
import logging

# Create and configure logger
logging.basicConfig(filename="merchant.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Test messages
logger.debug("Harmless debug Message")
logger.info("Just an information")
logger.warning("Its a Warning")
logger.error("Did you try to divide by zero")
logger.critical("Internet is down")


# Main function
def main():

    df = pd.read_csv("merchant_api.csv")
    # define a variable to store the previous url and status and status code
    previous_url = ''
    previous_status = ''
    previous_status_code = ''
    # iterate over the merchants and update the status
    for index, row in df.iterrows():
        # print the index
        print('Merchant Number: ', index)
        # get the url
        url = row['Endpoint']
        # check if the url is same as previous url
        if url == previous_url:
            # print the same url as previous Merchant
            print('Same URL as previous Merchant')
            # if same then update the reachable status as previous merchant
            df.at[index, 'Online'] = previous_status
            df.at[index, 'Status Code'] = previous_status_code
            # continue to next iteration
            continue
        # check if the url is empty
        if url == '':
            # if empty then update the reachable status as empty
            print('Empty URL')
            df.at[index, 'Online'] = 'empty'
            # continue to next iteration
            continue
        # if not same then update the previous url
        previous_url = url
        # check if the url is reachable or not
        try:
            # send the request to the url ignoring the SSL certificate
            r = requests.get(url, timeout=2, verify=False)
            # update the previous status and status code
            previous_status_code = r.status_code
            # if reachable then update the status as reachable
            print(r.status_code)
            # Convert response text to string
            response_text = str(r.text)
            # If status code is 200 then update the status as reachable
            if r.status_code == 200:
                df.at[index, 'Online'] = 'YES'
                df.at[index, 'Status Code'] = r.status_code
                df.at[index, 'Comment'] = response_text
                logger.info("Merchant is reachable")
                logger.info(r.text)
            # If status code is not 200 then update the status as not reachable but Online
            else:
                df.at[index, 'Online'] = 'YES'
                df.at[index, 'Status Code'] = r.status_code
                df.at[index, 'Comment'] = response_text
                logger.warning(
                    "Merchant is reachable but status code is not 200")
                logger.info(r.text)

        # except the timeout exception
        except requests.exceptions.Timeout:
            # if not reachable then update the Online status with status code
            print('Error: Timeout')
            # update the status as ERROR
            df.at[index, 'Online'] = 'NO'
            # update the Comment with error message
            df.at[index, 'Comment'] = 'Timeout'
            logger.error("Timeout")
            previous_status_code = ''
        # except the connection error exception
        except requests.exceptions.ConnectionError:
            # if not reachable then update the Online status with status code
            print('Error: Connection Error')
            # update the status as ERROR
            df.at[index, 'Online'] = 'ERROR'
            df.at[index, 'Comment'] = 'Connection Error'
            logger.error("Connection Error")
            previous_status_code = ''
        # except all other the exceptions
        except Exception as e:
            # if not reachable then update the Online status with status code
            print('Error: Host not reachable')
            df.at[index, 'Online'] = 'ERROR'
            df.at[index, 'Comment'] = e
            logger.critical("Host not reachable")
            logger.critical(e)
            previous_status_code = ''
        # update the previous status
        previous_status = df.at[index, 'Online']

    # write the updated csv file
    print('Writing the updated csv file')
    logger.info("Writing the updated csv file")
    df.to_csv('merchant_api.csv', index=False)

def handle_error(error_type, index, comment, logger, df):
    status = 'ERROR'
    if error_type == requests.exceptions.Timeout:
        status = 'NO'
    elif error_type == requests.exceptions.ConnectionError:
        comment = 'Connection Error'
    df.at[index, 'Online'] = status
    df.at[index, 'Comment'] = comment
    logger.error(comment)

# call the main function
if __name__ == '__main__':
    main()
