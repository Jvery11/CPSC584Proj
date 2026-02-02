from picrawler import Picrawler
from time import sleep

crawler = Picrawler() 

# simple functions to move picrawler in a square
# sleep should be set to 0.05
def main():  
    
    speed = 80
          
    while True:
        crawler.do_action('turn left angle', 3, speed)
        sleep(0.05)
    
        sleep(1)

if __name__ == "__main__":
    main()
