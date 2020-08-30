import pandas as pd
import random
import matplotlib.pyplot as plt


def load_excel(file_path: str):
    """
    Load csv file to data frame
    :param file_path: path to excel file
    :return: dict of pandas DataFrames
    """
    files = pd.read_csv(file_path)
    return files


def draw_scatter(df: pd.DataFrame, excluded: list, include: list):
    supp = []
    conf = []
    lift = []
    for idx, row in df.iterrows():
        if row.get('1') < row.get('2') not in excluded:
            if include.__len__() == 0 or (row.get('1') in include or row.get('2') in include):
                supp.append(row.get(key='supp'))  # + 0.0025 * (random.randint(1,10) - 5))
                conf.append(row.get(key='conf'))  # + 0.0025 * (random.randint(1,10) - 5))
                lift.append(row.get(key='lift'))
    plt.figure(1)
    plt.scatter(supp, conf, c=lift, cmap=plt.get_cmap('Blues'), alpha=0.5)
    plt.xlabel('Wsparcie')
    plt.ylabel('Zaufanie')
    cbar = plt.colorbar()
    cbar.set_label('Przyrost')
    return


def draw_scatter_labels(df: pd.DataFrame, x_low_limit: float, y_low_limit: float, excluded: list, include: list):
    supp = []
    conf = []
    lift = []
    labels = []
    for idx, row in df.iterrows():
        if row.get('1') < row.get('2') not in excluded and \
                row.get(key='supp') >= x_low_limit and row.get(key='conf') >= y_low_limit:
            if include.__len__() == 0 or (row.get('1') in include or row.get('2') in include):
                labels.append(f'{int(row.get("1"))}, {int(row.get(key="2"))}')
                supp.append(row.get(key='supp') + 0.0005 * (random.randint(-5, 5)))
                conf.append(row.get(key='conf') + 0.0005 * (random.randint(-5, 5)))
                lift.append(row.get(key='lift') + 0.0005 * (random.randint(-5, 5)))
    plt.figure(2)
    plt.scatter(supp, conf, c=lift, cmap=plt.get_cmap('Blues'), alpha=0.5, edgecolors='black')
    plt.xlabel('Wsparcie')
    plt.ylabel('Zaufanie')
    cbar = plt.colorbar()
    cbar.set_label('Przyrost')
    for idx, label in enumerate(labels):
        plt.annotate(label, (supp[idx], conf[idx]))
    return


def draw_bar(df: pd.DataFrame):
    df = df.drop(df[df['count'] < 40000].index)
    fig = plt.figure(3)
    plt.bar(x=df['distance'], height=df['count'])
    fig.set_xticks(np.arrange(0, 300, 1))
    plt.xlabel('Odległość')
    plt.ylabel('Liczebność')
    return


def main():
    filename = 'apriori_lipid_p_40.csv'
    df = load_excel(file_path='apriori_lipid/' + filename)
    exclude = []
    # include = []
    include = [28, 42, 56, 26, 154, 70, 18, 44, 30, 40, 84, 58, 98, 110, 112, 54, 74, 46, 24, 68]
    draw_scatter(df, excluded=exclude, include=include)
    draw_scatter_labels(df=df, x_low_limit=0, y_low_limit=0, excluded=exclude, include=include)

    # df_bar = load_excel(file_path='global_counts/global_count_p_10.csv')
    # draw_bar(df_bar)
    plt.show()


if __name__ == '__main__':
    main()
