# Testing the Endpoint API is reachable or not
# Author: DaTi_Co

# import the necessary packages
import requests
import pandas as pd
import logging
# import datetime

# Create and configure logger
# now = datetime.datetime.now()
# logfilename = now.strftime("%Y-%m-%d-%H-%M-%S") + '.log'
logfilename = 'endpoint-check.log'
logging.basicConfig(filename=logfilename,
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Test messages
logger.info("Logging started")

# define CSV file path
CSV = 'endpoint_api.csv'

# Main function
def main():
    # read the csv file
    df = pd.read_csv(CSV)
    # define a variable to store the previous url and status and status code
    previous_url = ''
    previous_status = ''
    previous_status_code = ''
    # iterate over the Endpoint and update the status
    for index, row in df.iterrows():
        # print the index
        print('Endpoint Number: ', index)
        # get the url
        url = row['Endpoint']
        # check if the url is same as previous url
        if url == previous_url:
            # print the same url as previous Endpoint
            print('Same URL as previous Endpoint')
            # if same then update the reachable status as previous Endpoint
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
            # Check request type
            request_type = row['GET/POST']
            # If request type is POST
            if request_type == 'POST':
                # Send the request to the url ignoring the SSL certificate
                r = requests.post(url, timeout=2, verify=False)
            # else request type is GET
            else:
                # Send the request to the url ignoring the SSL certificate
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
                logger.info("Endpoint is reachable")
                logger.info(r.text)
            # If status code is not 200 then update the status as not reachable but Online
            else:
                df.at[index, 'Online'] = 'YES'
                df.at[index, 'Status Code'] = r.status_code
                df.at[index, 'Comment'] = response_text
                logger.warning(
                    "Endpoint is reachable but status code is not 200")
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
    df.to_csv(CSV, index=False)

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
