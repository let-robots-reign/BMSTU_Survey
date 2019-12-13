import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from statistics import median


def get_good_reviews(data):
    return [len(list(filter(lambda x: x in ["Планирую заниматься", "Занимался, в основном положительный опыт",
                                            "Занимался, все понравилось"], review))) for review in data]


def get_prediction(x, y):
    X = pd.Series(x).values.reshape(-1, 1)
    Y = pd.Series(y).values.reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)
    return X, Y, Y_pred


def draw_pie_chart(data, title):
    options = {option: 0 for option in set(data)}
    for item in data:
        options[item] = options.get(item, 0) + 1

    keys = list(options.keys())
    values = list(options.values())

    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(pct / 100. * np.sum(allvals))
        return "{:.1f}%".format(pct, absolute)

    wedges, texts, autotexts = ax.pie(values, autopct=lambda pct: func(pct, values),
                                      textprops=dict(color="w"))

    ax.legend(wedges, keys, title="Варианты ответа", loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1), prop={"size": 10})

    plt.setp(autotexts, size=10, weight="bold")
    ax.set_title(title)
    plt.savefig("output/{}".format(title), bbox_inches="tight")
    #plt.show()


def draw_bar_chart(data, title):
    options = {option: 0 for option in set(data)}
    for item in data:
        options[item] = options.get(item, 0) + 1

    keys = list(options.keys())
    values = list(options.values())

    plt.figure(figsize=(15, 10))
    plt.bar(keys, values, width=0.3)
    plt.title("Лучшие предметы для изучения онлайн")

    plt.savefig("output/{}".format(title), bbox_inches="tight")
    #plt.show()


def draw_horizontal_bars(data):
    platforms = [x[0] for x in data]
    good_reviews = [x[1] for x in data]

    plt.figure(figsize=(15, 10))
    y_pos = np.arange(len(platforms))
    plt.barh(y_pos, good_reviews, align="center")
    plt.yticks(y_pos, platforms)
    plt.xlabel("Количество положительных отзывов")
    plt.title("Популярность разных платформ")

    plt.savefig("output/Популярность платформ", bbox_inches="tight")
    #plt.show()


def draw_popularity_charts(platforms, data):
    # для каждой платформы возьмем медианный отзыв, кроме "не слышал"
    opinions_to_numbers = {"Абсолютно неинтересно": -3, "Интересно, но отталкивает стоимость": -2,
                         "Занимался, но не понравилось": -1, "Планирую заниматься": 1,
                         "Занимался, в основном положительный опыт": 2, "Занимался, все понравилось": 3}

    reviews = [sorted([opinions_to_numbers[x] for x in review if x != "Не слышал"]) for review in data]
    median_reviews = list(map(median, reviews))
    # сортируем платформы по полученному медианному значению
    sorted_data = sorted(zip(platforms, median_reviews), key=lambda x: x[1])

    keys = [x[0] for x in sorted_data]
    values = [x[1] for x in sorted_data]

    plt.figure(figsize=(15, 10))
    plt.ylim(-4, 3)
    plt.scatter(keys, values)
    plt.yticks(range(-3, 4), opinions_to_numbers.keys())
    plt.xlabel("Название платформы")
    plt.title("Медианная оценка платформы")

    # сделаем линейную регрессию
    platforms_indices = range(len(platforms))
    X, Y, pred = get_prediction(platforms_indices, values)

    plt.scatter(X, Y)
    plt.plot(X, pred)

    plt.savefig("output/Медианная оценка платформы", bbox_inches="tight")
    #plt.show()

    # теперь посчитаем долю хороших отзывов от всех отзывов
    good_reviews_share = [x / 40 for x in get_good_reviews(data)]
    sorted_data = sorted(zip(platforms, good_reviews_share), key=lambda x: x[1])

    keys = [x[0] for x in sorted_data]
    values = [x[1] for x in sorted_data]

    plt.figure(figsize=(15, 10))
    plt.ylim(0, 0.6)
    plt.scatter(keys, values)
    plt.xlabel("Название платформы")
    plt.title("Доля положительных отзывов платформы")

    # сделаем линейную регрессию
    platforms_indices = range(len(platforms))
    X, Y, pred = get_prediction(platforms_indices, values)

    plt.scatter(X, Y)
    plt.plot(X, pred)
    plt.savefig("output/Доля положительных отзывов", bbox_inches="tight")
    #plt.show()


def parse_data(data):
    questions = data.columns[1:]
    answers = []

    for question in questions:
        cur_answers = data[question]
        answers.append(list(cur_answers))

    answers[-6] = [x[:x.find(" (")] for x in ";".join(answers[-6]).split(";")]  # нормализуем ответ с multiple choice

    titles = ["Пол", "Образование", "Тип населенного пункта", "Опыт онлайн-обучения", "Coursera", "Stepik",
              "Edx", "GeekBrains", "Udacity", "Udemy", "Открытое образование", "Фоксфорд", "Важнейший критерий",
              "Лучшие предметы", "Форма материалов", "Отношение к дедлайнам", "Из-за чего люди бросают курсы",
              "Смотрят ли работодатели на сертификаты", "Сможет ли заменить очное образование"]

    for i in range(len(answers)):
        if i == 13:  # вопрос, по которому строить bar chart
            draw_bar_chart(answers[i], titles[i])
        elif not 4 <= i <= 11:  # вопросы, по которым строить pie chart
            draw_pie_chart(answers[i], titles[i])

    platforms = ["Coursera", "Stepik", "Edx", "GeekBrains", "Udacity", "Udemy", "Открытое образование", "Фоксфорд"]
    good_reviews_number = get_good_reviews(answers[4:12])

    # сортируем платформы по количеству положительных отзывов
    sorted_data = sorted(zip(platforms, good_reviews_number), key=lambda x: x[1])
    draw_horizontal_bars(sorted_data)

    draw_popularity_charts(platforms, answers[4:12])


def main():
    filename = "online_courses.csv"
    data = pd.read_csv(filename)
    parse_data(data)


if __name__ == "__main__":
    main()
