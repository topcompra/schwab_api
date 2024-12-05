import logging


from spx_monthly_seasonality import main as main_file1
from spx_weekly_seasonality import main as main_file2
from spx_daily_seasonality import main as main_file3

#from backtesting import main as main_file4


from main_login import AuthenticationManager, client_id, client_secret
import asyncio
import time
import logging
from functions_timer_decorator import timeit


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@timeit
def run_all_files():

    auth_manager = AuthenticationManager(client_id=client_id, client_secret=client_secret)

    
    logging.info("Starting execution of file1...")
    main_file1(auth_manager)  # Run file1's main function
    logging.info("Finished execution of file1.")
    
    logging.info("\nStarting execution of file2...")
    main_file2(auth_manager)  # Run file2's main function
    logging.info("Finished execution of file2.")
    
    logging.info("\nStarting execution of file3...")
    main_file3(auth_manager)  # Run file3's main function
    logging.info("Finished execution of file3.")



'''
# Convert this function to be asynchronous to run sequentially
@timeit
async def run_all_files_async():

    auth_manager = AuthenticationManager(client_id=client_id, client_secret=client_secret)

    logging.info("Starting execution of file1...")
    await asyncio.to_thread(main_file1, auth_manager) # Run file1's main function and convert normal function to async def 
    logging.info("Finished execution of file1.")

    logging.info("\nStarting execution of file2...")
    await asyncio.to_thread(main_file2, auth_manager) # Run file1's main function and convert normal function to async def 
    logging.info("Finished execution of file2.")

    logging.info("\nStarting execution of file3...")
    await asyncio.to_thread(main_file3, auth_manager)  # Run file1's main function and convert normal function to async def 
    logging.info("Finished execution of file3.")

'''


if __name__ == "__main__":
    run_all_files()
    #asyncio.run(run_all_files_async())