
get_ipython().run_line_magic('pylab', 'inline')
from matplotlib import pyplot as plt
import datetime
import time

global t1

now = datetime.datetime.now()
time_now2 = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + "  " +             str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

print("Hello !")
print("Enter the page number of studying book to track your studying more efficient")
print("To see which pages have you read so far type 99999")
print("To finish it, type 1000000")

page_list, sum_list, x_list, y_list_minute, y_list_second = [], [], [], [], []
number_of_page, status = 0, 0
dic_data = {}
page_number = ""

name_subject = input("what subject do you want to study ?")

first_time = time.time()

first_text_file = open("time_reading_log.txt", "a")
first_text_file.write(" \n")
first_text_file.write("=" * 60 + str(time_now2) + " " + str(name_subject) + "=" * 78 + "\n")
first_text_file.write(" \n")
first_text_file.close()

def benvisesh():
    first_text_file2 = open("time_reading_log.txt", "a")
    first_text_file2.write("you read page ({0:<4}) in [{1:<3}] second\t".
                           format(page_number, round(t1 - first_time)))
    first_text_file2.write("You studied ({0:<2}) pages in [{1:2} minutes and {2:2} seconds]\t".
                           format(len(dic_data), total_time // 60, total_time % 60))
    first_text_file2.write(("max = {0} Sec, min ={1} Sec, average = {2} Sec\t".
                            format(max_time_second, min_time_second, average_time_second)))
    first_text_file2.write("your status {0:3} %\n".
                           format(round(status)))
    first_text_file2.close()

while page_number != 1000000:

    while True:
        try:
            page_number = int(input("Page >>"))
            if page_number not in page_list and page_number != 0:
                break
            else:
                if page_number == 0:
                    print("0  is not a valid for page number")
                else:
                    print("page {} was entered before".
                          format(page_number))
                continue
        except ValueError:

            print("is not a valid page number")
            continue

    if page_number == 99999:
        print("you read: {} pages".format(len(page_list)))
        for page in page_list:
            print("page : {}".format(page))
        continue

    page_list.append(page_number)
    number_of_page += 1
    if page_number == 1000000:
        continue

    t1 = time.time()
    deltatime = round(t1 - first_time)
    dic_data.update({page_number: deltatime})
    y_list_minute.append(round(deltatime / 60, 1))
    y_list_second.append(deltatime)
    x_list.append(number_of_page)
    total_time = sum(y_list_second)
    sum_list.append(round(total_time/60, 2))
    max_time_second = max(y_list_second)
    min_time_second = min(y_list_second)
    average_time_second = round(total_time / len(y_list_second))
    average_time_minute = round((total_time / len(y_list_second))/60, 1)

    if deltatime > average_time_second:
        status = 50 - (50 * (deltatime - average_time_second)) / (max_time_second - average_time_second)
    elif deltatime < average_time_second:
        status = 50 + (50 * (average_time_second - deltatime)) / (average_time_second - min_time_second)
    else:
        status = 50

    if status > 100:
        status = 100
    if status < 0:
        status = 0

    print("Page {0} in {1} Min & {2} Sec".
          format(page_number, deltatime//60, deltatime % 60))
    print("You studied {0} pages in {1} minutes and {2} seconds".
          format(len(dic_data), (total_time // 60), (total_time % 60)))
    print("max = {0} Min & {1} Sec, min = {2} Min & {3} Sec, average = {4} Min & {5} Sec".
          format(max_time_second//60, max_time_second % 60, min_time_second//60,
                 min_time_second % 60, average_time_second//60, average_time_second % 60))
    print("your status {0} %".
          format(round(status)))

    benvisesh()
    # benvisesh1()
    first_time = t1
    print()

    plt.subplot(2, 1, 1)
    # plt.figure(figsize=(10,8))

    plt.step(x_list, y_list_minute, '--', color="black", lw=1)
    plt.title("[{0} pages in {1} Min & {2} Sec] [{3} Min/Page] [{4}]".
              format(len(dic_data), round(total_time // 60), round(total_time % 60), average_time_minute, name_subject))
    plt.ylabel("Time (Min)")
    if len(x_list) < 6:

        plt.xticks(x_list)
        plt.yticks(y_list_minute)

    cm = plt.cm.get_cmap('rainbow')
    plot = plt.scatter(x_list, y_list_minute, c=y_list_minute, marker='o', s=30, lw=1, cmap=cm)
    plt.colorbar(plot).set_label('minutes per page')

    plt.subplot(2, 1, 2)

    plt.plot(x_list, sum_list,  'b--')
    plt.xlabel("Pages     [{}/{:02}/{:02}] Time [{:02}:{:02}] till [{:02}:{:02}]"
               .format(now.year, now.month, now.day, now.hour, now.minute,
                       datetime.datetime.now().hour, datetime.datetime.now().minute))
    plt.ylabel('Accumulation time (Min)')
    if len(x_list) < 6:
        plt.xticks(x_list)
        plt.yticks(sum_list)
    plt.grid()
    plt.savefig("Graphs {}_{:02}_{:02} ({}-{}-{}).png"
                .format(now.year, now.month, now.day, now.hour, now.minute, now.second))

    plt.show()

