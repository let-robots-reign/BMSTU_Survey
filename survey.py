import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def draw_pie_chart(data, title):
    options = {option: 0 for option in set(data)}
    for item in data:
        options[item] = options.get(item, 0) + 1

    keys = list(options.keys())
    values = list(options.values())

    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(pct / 100. * np.sum(allvals))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    wedges, texts, autotexts = ax.pie(values, autopct=lambda pct: func(pct, values),
                                      textprops=dict(color="w"))

    ax.legend(wedges, keys, title="Варианты ответа", loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1), prop={"size": 10})

    plt.setp(autotexts, size=10, weight="bold")
    ax.set_title(title)
    plt.savefig("output/{}".format(title), bbox_inches="tight")
    #plt.show()


def draw_bar_chart(data, title):
    pass


def draw_horizontal_bars(data):
    platforms = [x[0] for x in data]
    good_reviews = [x[1] for x in data]

    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw=dict(aspect="equal"))

    y_pos = np.arange(len(platforms))

    ax.barh(y_pos, good_reviews, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(platforms)
    ax.set_xlabel('Количество положительных отзывов')
    ax.set_title('Популярность разных платформ')

    plt.savefig("output/Популярность платформ")
    #plt.show()


def parse_data(data):
    questions = data.columns[1:]
    answers = []

    for question in questions:
        cur_answers = data[question]
        answers.append(list(cur_answers))

    answers[-6] = ";".join(answers[-6]).split(";")

    titles = ["Пол", "Образование", "Тип населенного пункта", "Опыт онлайн-обучения", "Coursera", "Stepik",
              "Edx", "GeekBrains", "Udacity", "Udemy", "Открытое образование", "Фоксфорд", "Важнейший критерий",
              "Лучшие предметы", "Форма материалов", "Отношение к дедлайнам", "Из-за чего люди бросают курсы",
              "Смотрят ли работодатели на сертификаты", "Сможет ли заменить очное образование"]

    for i in range(len(answers)):
        if not 4 <= i <= 11:  # вопросы, по которым строить pie chart
            draw_pie_chart(answers[i], titles[i])  # вопросы, по которым строить pie charts

    platforms = ["Coursera", "Stepik", "Edx", "GeekBrains", "Udacity", "Udemy", "Открытое образование", "Фоксфорд"]
    good_reviews_number = [len(list(filter(lambda x: x in ["Планирую заниматься", "Занимался, в основном положительный опыт",
                                            "Занимался, все понравилось"], review))) for review in answers[4:12]]

    # сортируем платформы по количеству положительных отзывов
    data = sorted(zip(platforms, good_reviews_number), key=lambda x: x[1])
    draw_horizontal_bars(data)

    return answers


def main():
    filename = "online_courses.csv"
    data = pd.read_csv(filename)
    result = parse_data(data)
    print(result)


if __name__ == "__main__":
    main()
