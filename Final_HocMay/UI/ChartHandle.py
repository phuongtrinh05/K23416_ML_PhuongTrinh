import seaborn as sns

class ChartHandle:
    # =============================
    # 🔹 Tạo hiệu ứng "explode" cho Pie Chart
    # =============================
    def getExplode(self, df, columnLabel):
        """
        Tự động tạo danh sách explode: phần tử đầu tiên nhô ra 0.1, còn lại 0
        """
        explode = [0.1]
        for _ in range(len(df[columnLabel]) - 1):
            explode.append(0)
        return explode

    # =============================
    # 🔹 Biểu đồ Tròn (Pie Chart)
    # =============================
    def visualizePieChart(self, figure, canvas, df, columnLabel, columnStatistic, title, legend=True):
        explode = self.getExplode(df, columnLabel)
        figure.clear()
        ax = figure.add_subplot(111)
        ax.pie(df[columnStatistic], labels=df[columnLabel], autopct='%1.2f%%', explode=explode)
        if legend:
            ax.legend(df[columnLabel], loc='lower right')
        ax.set_title(title)
        canvas.draw()

    # =============================
    # 🔹 Biểu đồ Đường (Line Plot)
    # =============================
    def visualizeLinePlotChart(self, figure, canvas, df, columnX, columnY, title, hue=None, xticks=False):
        figure.clear()
        ax = figure.add_subplot(111)
        ax.ticklabel_format(useOffset=False, style="plain")
        ax.grid()
        sns.lineplot(data=df, x=columnX, y=columnY, marker='o', color='orange', hue=hue, ax=ax)
        ax.set_xlabel(columnX)
        ax.set_ylabel(columnY)
        ax.set_title(title)
        ax.legend(loc='lower right')

        # Tùy chọn hiển thị tên tháng nếu là dữ liệu theo tháng
        if xticks:
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        canvas.draw()

    # =============================
    # 🔹 Biểu đồ Cột đơn giản (Bar Chart)
    # =============================
    def visualizeBarChart(self, figure, canvas, df, columnX, columnY, title):
        figure.clear()
        ax = figure.add_subplot(111)
        ax.ticklabel_format(useOffset=False, style="plain")
        ax.grid()
        ax.bar(df[columnX], df[columnY], color='skyblue')
        ax.set_title(title)
        ax.set_xlabel(columnX)
        ax.set_ylabel(columnY)
        canvas.draw()

    # =============================
    # 🔹 Biểu đồ Cột nhóm theo phân loại (Bar Plot)
    # =============================
    def visualizeBarPlot(self, figure, canvas, df, columnX, columnY, hueColumn, title, alpha=0.8, width=0.6):
        figure.clear()
        ax = figure.add_subplot(111)
        ax.ticklabel_format(useOffset=False, style="plain")
        ax.grid()
        sns.barplot(data=df, x=columnX, y=columnY, hue=hueColumn, alpha=alpha, width=width, ax=ax)
        ax.set_title(title)
        ax.set_xlabel(columnX)
        ax.set_ylabel(columnY)
        canvas.draw()

    # =============================
    # 🔹 Biểu đồ Cột nhiều nhóm (Count Plot)
    # =============================
    def visualizeMultiBarChart(self, figure, canvas, df, columnX, columnY, hueColumn, title):
        figure.clear()
        ax = figure.add_subplot(111)
        ax.ticklabel_format(useOffset=False, style="plain")
        ax.grid()
        sns.countplot(x=columnX, hue=hueColumn, data=df, ax=ax)
        ax.set_title(title)
        ax.set_xlabel(columnX)
        ax.set_ylabel(columnY)
        canvas.draw()

    # =============================
    # 🔹 Biểu đồ Phân tán (Scatter Plot)
    # =============================
    def visualizeScatterPlot(self, figure, canvas, df, columnX, columnY, title):
        figure.clear()
        ax = figure.add_subplot(111)
        ax.ticklabel_format(useOffset=False, style="plain")
        ax.grid()
        sns.scatterplot(data=df, x=columnX, y=columnY, ax=ax, color='salmon')
        ax.set_title(title)
        ax.set_xlabel(columnX)
        ax.set_ylabel(columnY)
        canvas.draw()
