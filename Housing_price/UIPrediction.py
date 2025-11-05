from tkinter import *
from tkinter import messagebox, ttk
from tkinter.font import Font
from tkinter import filedialog as fd
from DataSetViewer import DataSetViewer
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from FileUtil import FileUtil
import os
from datetime import datetime

class UIPrediction:
    fileName = ""

    def __init__(self):
        pass

    def create_ui(self):
        self.root = Tk()
        self.root.title("House Pricing Prediction- Faculty of Information Systems")
        self.root.geometry("1500x850")
        main_panel = PanedWindow(self.root)
        main_panel["bg"] = "yellow"
        main_panel.pack(fill=BOTH, expand=True)

        top_panel = PanedWindow(main_panel, height=80)
        top_panel["bg"] = "blue"
        main_panel.add(top_panel)
        top_panel.pack(fill=X, side=TOP, expand=False)

        font = Font(family="tahoma", size=18)
        title_label = Label(top_panel, text='House Pricing Prediction', font=font)
        title_label["bg"] = "yellow"
        top_panel.add(title_label)

        center_panel = PanedWindow(main_panel)
        main_panel.add(center_panel)
        center_panel["bg"] = "pink"
        center_panel.pack(fill=BOTH, expand=True)

        choose_dataset_panel = PanedWindow(center_panel, height=30)
        center_panel.add(choose_dataset_panel)
        choose_dataset_panel["bg"]="orange"
        choose_dataset_panel.pack(fill=X)

        dataset_label=Label(choose_dataset_panel,text="Select Dataset:")
        self.selectedFileName = StringVar()
        self.selectedFileName.set("dataset/USA_Housing.csv")
        self.choose_dataset_entry=Entry(choose_dataset_panel,textvariable=self.selectedFileName)
        self.choose_dataset_button = Button(choose_dataset_panel, text="1.Pick Dataset",
                                            width=10,command=self.do_pick_data)
        self.view_dataset_button = Button(choose_dataset_panel, text="2.View Dataset", width=20,
                                          command=self.do_view_dataset)
        choose_dataset_panel.add(dataset_label)
        choose_dataset_panel.add(self.choose_dataset_entry)
        choose_dataset_panel.add(self.choose_dataset_button)
        choose_dataset_panel.add(self.view_dataset_button)
        self.view_dataset_button.pack(side=RIGHT, expand=False)
        self.choose_dataset_button.pack(side=RIGHT, expand=False)

        #Training Rate
        training_rate_panel = PanedWindow(center_panel, height=30)
        center_panel.add(training_rate_panel)
        training_rate_panel.pack(fill=X)
        training_rate_label = Label(training_rate_panel, text="Training Rate:")
        self.training_rate = IntVar()
        self.training_rate.set(80)
        self.training_rate_entry = Entry(training_rate_panel, textvariable=self.training_rate,width=20)
        training_rate_panel.add(training_rate_label)
        training_rate_panel.add(self.training_rate_entry)
        percent_label=Label(text="%",width=20,anchor="w", justify=LEFT)
        percent_label.pack(side=RIGHT,expand=False,fill=X)
        training_rate_panel.add(percent_label)
        self.train_model_button=Button(training_rate_panel,text="3.Train Model",width=20,command=self.do_train)
        training_rate_panel.add(self.train_model_button)
        self.evaluate_model_button = Button(training_rate_panel, text="4.Evaluate Model",
                                            width=20,command=self.do_evaluation)
        training_rate_panel.add(self.evaluate_model_button)
        self.status=StringVar()
        self.train_model_result_label = Label(training_rate_panel,textvariable=self.status)
        training_rate_panel.add(self.train_model_result_label)

        evaluate_panel=PanedWindow(center_panel,height=400)
        center_panel.add(evaluate_panel)
        evaluate_panel["bg"]="cyan"
        center_panel.add(evaluate_panel)

        evaluate_panel.pack(fill=X)

        table_evaluate_panel=PanedWindow(evaluate_panel,height=400)
        evaluate_panel.add(table_evaluate_panel)

        # define columns
        columns = ('Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
                    'Avg. Area Number of Bedrooms', 'Area Population', 'Original Price', 'Prediction Price')

        self.tree = ttk.Treeview(table_evaluate_panel, columns=columns, show="headings")

        self.tree.column("# 1", anchor=CENTER, stretch=NO, width=120)
        self.tree.column("# 2", anchor=CENTER, stretch=NO, width=120)
        self.tree.column("# 3", anchor=CENTER, stretch=NO, width=120)
        self.tree.column("# 4", anchor=CENTER, stretch=NO, width=120)
        self.tree.column("# 5", anchor=CENTER, stretch=NO, width=120)
        self.tree.column("# 6", anchor=CENTER, stretch=NO, width=120)
        self.tree.column("# 7", anchor=CENTER, stretch=NO, width=120)

        # define headings
        self.tree.heading("Avg. Area Income", text="Avg. Area Income")
        self.tree.heading("Avg. Area House Age", text="Avg. Area House Age")
        self.tree.heading("Avg. Area Number of Rooms", text="Avg. Area Number of Rooms")
        self.tree.heading("Avg. Area Number of Bedrooms", text="Avg. Area Number of Bedrooms")
        self.tree.heading("Area Population", text="Area Population")
        self.tree.heading("Original Price", text="Original Price")
        self.tree.heading("Prediction Price", text="Prediction Price")
        # self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = ttk.Scrollbar(table_evaluate_panel, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        # scrollbar.grid(row=0, column=1, sticky="ns")
        scrollbar.pack(side=RIGHT, fill=BOTH, expand=True)

        coefficient_panel=PanedWindow(evaluate_panel)
        coefficient_panel["bg"]="pink"
        coefficient_panel.pack(side=RIGHT,fill=X,expand=False)
        evaluate_panel.add(coefficient_panel)

        coefficient_detail_label=Label(coefficient_panel,text="Coefficient:")
        coefficient_panel.add(coefficient_detail_label)
        coefficient_detail_label.pack(side=TOP,fill=X,expand=False)
        coefficient_detail_panel=PanedWindow(coefficient_panel)
        coefficient_panel.add(coefficient_detail_panel)
        coefficient_detail_panel.pack(side=TOP,expand=False,fill=X)

        self.coefficient_detail_text = Text(coefficient_detail_panel, height=12,width=50)
        scroll = Scrollbar(coefficient_detail_panel)
        self.coefficient_detail_text.configure(yscrollcommand=scroll.set)
        self.coefficient_detail_text.pack(side=LEFT,expand=False,fill=X)

        scroll.config(command=self.coefficient_detail_text.yview)
        scroll.pack(side=RIGHT, fill=Y, expand=True)

        metric_panel=PanedWindow(coefficient_panel,height=30)
        coefficient_panel.add(metric_panel)
        metric_panel.pack(side=TOP,fill=BOTH,expand=True)

        self.mae_value=DoubleVar()
        mae_label=Label(metric_panel,text="Mean Absolute Error(MAE):")
        mae_label.grid(row=0,column=0)
        mae_entry = Entry(metric_panel, text="", width=20,textvariable=self.mae_value)
        mae_entry.grid(row=0, column=1)

        self.mse_value = DoubleVar()
        mse_label = Label(metric_panel, text="Mean Square Error(MSE):")
        mse_label.grid(row=1, column=0)
        mse_entry = Entry(metric_panel, text="", width=20,textvariable=self.mse_value)
        mse_entry.grid(row=1, column=1)

        self.rmse_value = DoubleVar()
        rmse_label = Label(metric_panel, text="Root Mean Square Error(RMSE):")
        rmse_label.grid(row=2, column=0)
        rmse_entry = Entry(metric_panel, text="", width=20,textvariable=self.rmse_value)
        rmse_entry.grid(row=2, column=1)

        savemodel_button = Button(metric_panel, text="5. Save Model", width=20,command=self.do_save_model)
        savemodel_button.grid(row=3,column=1)

        loadmodel_panel = PanedWindow(center_panel, height=20)
        loadmodel_panel["bg"] = "yellow"
        loadmodel_panel.pack(fill=BOTH, side=TOP)

        # biến StringVar để lưu tên model đang chọn
        self.model_var = StringVar()
        self.model_var.set("")

        # OptionMenu liệt kê các model đã lưu
        # Nút Load Model ở bên trái
        loadmodel_button = Button(loadmodel_panel, text="6. Load Model",
                                  command=self.do_load_model)
        loadmodel_button.grid(row=0, column=0, padx=5, pady=2)

        # OptionMenu ở bên phải
        self.model_option = OptionMenu(loadmodel_panel, self.model_var, "")
        self.model_option.grid(row=0, column=1, padx=5, pady=2)

        # sau khi tạo xong UI, tải danh sách model có sẵn
        self.refresh_model_list()

        input_prediction_panel = PanedWindow(center_panel)
        input_prediction_panel.pack(fill=BOTH, side=TOP,expand=True)

        area_income_label = Label(input_prediction_panel, text="Avg. Area Income:")
        area_income_label.grid(row=0, column=0)
        self.area_income_value=DoubleVar()
        area_income_entry = Entry(input_prediction_panel, text="", width=40,textvariable=self.area_income_value)
        area_income_entry.grid(row=0, column=1)

        area_house_age_label = Label(input_prediction_panel, text="Avg. Area House Age:")
        area_house_age_label.grid(row=1, column=0)
        self.area_house_age_value = DoubleVar()
        area_house_age_entry = Entry(input_prediction_panel, text="", width=40,textvariable=self.area_house_age_value)
        area_house_age_entry.grid(row=1, column=1)

        area_number_of_rooms_label = Label(input_prediction_panel, text="Avg. Area Number of Rooms:")
        area_number_of_rooms_label.grid(row=2, column=0)
        self.area_number_of_rooms_value=DoubleVar()
        area_number_of_rooms_entry = Entry(input_prediction_panel, text="", width=40,
                                           textvariable=self.area_number_of_rooms_value)
        area_number_of_rooms_entry.grid(row=2, column=1)

        area_number_of_bedrooms_label = Label(input_prediction_panel, text="Avg. Area Number of Bedrooms:")
        area_number_of_bedrooms_label.grid(row=3, column=0)
        self.area_number_of_bedrooms_value=DoubleVar()
        area_number_of_bedrooms_entry = Entry(input_prediction_panel, text="", width=40,
                                              textvariable=self.area_number_of_bedrooms_value)
        area_number_of_bedrooms_entry.grid(row=3, column=1)

        area_population_label = Label(input_prediction_panel, text="Area Population:")
        area_population_label.grid(row=4, column=0)
        self.area_population_value = DoubleVar()
        area_population_entry = Entry(input_prediction_panel, text="", width=40,
                                      textvariable=self.area_population_value)
        area_population_entry.grid(row=4, column=1)

        prediction_button=Button(input_prediction_panel,text="7. Prediction House Pricing",command=self.do_prediction)
        prediction_button.grid(row=5,column=1)

        prediction_price_label = Label(input_prediction_panel, text="Prediction Price:")
        prediction_price_label.grid(row=6, column=0)
        self.prediction_price_value=DoubleVar()
        prediction_price_entry = Entry(input_prediction_panel, text="", width=40,
                                       textvariable=self.prediction_price_value)
        prediction_price_entry.grid(row=6, column=1)

        designedby_panel = PanedWindow(main_panel, height=20)
        designedby_panel["bg"] = "cyan"
        designedby_panel.pack(fill=BOTH, side=BOTTOM)
        designedby_label = Label(designedby_panel, text="Designed by: Tran Duy Thanh")
        designedby_label["bg"] = "cyan"
        designedby_label.pack(side=LEFT)

        pass

    def show_ui(self):
        self.root.mainloop()

    def do_pick_data(self):
        filetypes=(("Dataset CSV","*.csv"),
                   ("All Files","*.*")
                   )
        s=fd.askopenfilename(
            title="Choose dataset",
            initialdir="/",
            filetypes=filetypes)
        self.selectedFileName.set(s)
        pass

    def do_view_dataset(self):
        viewer= DataSetViewer()
        viewer.create_ui()
        viewer.show_data_listview(self.selectedFileName.get())
        viewer.show_ui()
        pass

    def do_train(self):
        ratio=self.training_rate.get()/100
        self.df = pd.read_csv(self.selectedFileName.get())

        self.X = self.df[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms','Avg. Area Number of Bedrooms', 'Area Population']]
        self.y = self.df['Price']

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=1-ratio, random_state=101)

        from sklearn.linear_model import LinearRegression

        self.lm = LinearRegression()

        self.lm.fit(self.X_train, self.y_train)
        self.status.set("Trained is finished")
        messagebox.showinfo("infor","Trained is finished")
        pass

    def do_evaluation(self):
        # print the intercept
        # print(self.lm.intercept_)
        intercept=self.lm.intercept_

        self.coeff_df = pd.DataFrame(self.lm.coef_, self.X.columns, columns=['Coefficient'])
        print(self.coeff_df)
        self.coefficient_detail_text.insert(END, self.coeff_df)

        predictions = self.lm.predict(self.X_test)
        print(predictions)
        print(self.X_test)
        print("self.y_test:")
        print(self.y_test)
        y_test_array=np.asarray(self.y_test)
        for i in range(0,len(self.X_test)):
            values = [self.X_test.iloc[i][0], self.X_test.iloc[i][1], self.X_test.iloc[i][2], self.X_test.iloc[i][3],self.X_test.iloc[i][4], y_test_array[i],predictions[i]]
            print(values)
            self.tree.insert('', END, values=values)

        print('MAE:', metrics.mean_absolute_error(self.y_test, predictions))
        print('MSE:', metrics.mean_squared_error(self.y_test, predictions))
        print('RMSE:', np.sqrt(metrics.mean_squared_error(self.y_test, predictions)))

        self.mae_value.set(metrics.mean_absolute_error(self.y_test, predictions))
        self.mse_value.set(metrics.mean_squared_error(self.y_test, predictions))
        self.rmse_value.set(np.sqrt(metrics.mean_squared_error(self.y_test, predictions)))

        self.status.set("Evaluation is finished")
        messagebox.showinfo("infor", "Evaluation is finished")
        pass

    def do_save_model(self):
        # hỏi lại người dùng có chắc lưu model không
        if not hasattr(self, "lm"):
            messagebox.showwarning("infor", "Model chưa được train, không thể lưu!")
            return

        ans = messagebox.askyesno(
            "Confirm Save",
            "Bạn có chắc chắn muốn lưu mô hình hiện tại?\n"
            "Mỗi tỉ lệ train khác nhau sẽ cho chất lượng mô hình khác nhau."
        )
        if not ans:
            return

        # tạo tên file mới kèm ngày giờ hiện tại
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"housingmodel_{now_str}.zip"

        ok = FileUtil.savemodel(self.lm, filename)
        if ok:
            messagebox.showinfo("infor", f"Đã lưu mô hình thành công:\n{filename}")
            # cập nhật lại danh sách model cho OptionMenu
            self.refresh_model_list()
            # chọn luôn model vừa lưu
            self.model_var.set(filename)
        else:
            messagebox.showerror("Error", "Lưu mô hình thất bại!")

    def do_load_model(self):
        filename = self.model_var.get().strip()
        if not filename:
            messagebox.showwarning("infor", "Chưa chọn mô hình để nạp!")
            return

        model = FileUtil.loadmodel(filename)
        if model is None:
            messagebox.showerror("Error", f"Nạp mô hình {filename} thất bại!")
            return

        self.lm = model
        messagebox.showinfo("infor", f"Loading model từ file:\n{filename}\nthành công!")

    def do_prediction(self):
        result = self.lm.predict([[self.area_income_value.get(),
                                   self.area_house_age_value.get(),
                                   self.area_number_of_rooms_value.get(),
                                   self.area_number_of_bedrooms_value.get(),
                                   self.area_population_value.get()]])
        self.prediction_price_value.set(result[0])
        pass

    def get_model_list(self):
        """
        Trả về danh sách các file mô hình đã lưu.
        Ở đây em lấy tất cả file .zip bắt đầu bằng 'housingmodel_' trong thư mục hiện tại.
        """
        files = []
        for f in os.listdir("."):
            if f.startswith("housingmodel_") and f.endswith(".zip"):
                files.append(f)
        files.sort(reverse=True)  # mới nhất đứng trước
        return files

    def refresh_model_list(self):
        """
        Cập nhật lại OptionMenu với danh sách model hiện có.
        """
        models = self.get_model_list()
        menu = self.model_option["menu"]
        menu.delete(0, "end")

        if not models:
            # không có model nào
            self.model_var.set("")
            return

        for m in models:
            menu.add_command(label=m, command=lambda value=m: self.model_var.set(value))

        # đặt mặc định là model mới nhất
        self.model_var.set(models[0])


