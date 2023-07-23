import matplotlib.pyplot as plt

plt.rcParams['font.family'] = "Liberation Serif"
plt.rcParams['font.size'] = 18

groups = ["поиск"]

index = 1
width = 0.3

no_index_time = [50]
index_time = [12]

#rects1 = axes.bar(br1, data[0], width=bar_width, label='zstd',
#                    hatch='/', fill=False, edgecolor='b', lw=line_width)
plt.bar(index - width / 2, index_time, width-0.05,
        label="С индексом", hatch="\\", fill=False,
        edgecolor="g", lw=3)
plt.bar(index + width / 2, no_index_time, width-0.05,
        label="Без индекса", hatch='/', fill=False,
        edgecolor="r", lw=3)
plt.xlim([0, 2])
plt.xticks([index], groups)
plt.ylabel("время выполнения, ед.")

plt.grid()
plt.gca().set_axisbelow(True)
plt.legend(fontsize=14)
plt.show()

