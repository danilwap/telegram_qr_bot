import qrcode
import datetime



def main():
    start_time = datetime.datetime.now()
    qr = qrcode.make('https://cp.puzzlebot.top/', border=1, box_size=100)
    qr.save('text.png')
    print(datetime.datetime.now() - start_time)


if __name__ == '__main__':
    main()