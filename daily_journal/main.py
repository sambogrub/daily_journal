'''Main module for daily journal app. Will initialize the controller,
passing it both the repository and the ui'''
import ui
import model
import controller
import repository
import logger 

def main():
    logger.configure_logger()


if __name__ == '__main__':
    main()