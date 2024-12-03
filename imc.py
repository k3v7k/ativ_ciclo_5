# -*- coding: utf-8 -*-
import wx
import sqlite3

class IMCCalculator(wx.Frame):
    def __init__(self, *args, **kw):
        super(IMCCalculator, self).__init__(*args, **kw)
        self.InitUI()
        self.ConnectDatabase()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Título da janela
        self.SetTitle("Cálculo do IMC - Índice de Massa Corporal")

        # Nome do paciente
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        lbl_name = wx.StaticText(panel, label="Nome do Paciente:")
        hbox1.Add(lbl_name, flag=wx.RIGHT, border=8)
        self.txt_name = wx.TextCtrl(panel)
        hbox1.Add(self.txt_name, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Endereço Completo
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        lbl_address = wx.StaticText(panel, label="Endereço Completo:")
        hbox2.Add(lbl_address, flag=wx.RIGHT, border=8)
        self.txt_address = wx.TextCtrl(panel)
        hbox2.Add(self.txt_address, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        # Entrada de Altura
        lbl_height = wx.StaticText(panel, label="Altura (cm)")
        hbox3.Add(lbl_height, flag=wx.RIGHT, border=8)
        self.txt_height = wx.TextCtrl(panel, size=(100, -1))
        hbox3.Add(self.txt_height, flag=wx.RIGHT, border=10)

        # Entrada de Peso
        lbl_weight = wx.StaticText(panel, label="Peso (Kg)")
        hbox3.Add(lbl_weight, flag=wx.RIGHT, border=8)
        self.txt_weight = wx.TextCtrl(panel, size=(100, -1))
        hbox3.Add(self.txt_weight, flag=wx.RIGHT, border=10)

        # Área de Resultado
        result_box = wx.StaticBox(panel, label="Resultado")
        result_sizer = wx.StaticBoxSizer(result_box, wx.VERTICAL)
        self.result = wx.StaticText(panel, label="", style=wx.ALIGN_CENTER_VERTICAL)
        result_sizer.Add(self.result, flag=wx.ALIGN_LEFT | wx.RIGHT, border=10)
        hbox3.Add(result_sizer, proportion=1, flag=wx.EXPAND | wx.LEFT, border=10)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Botões
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        btn_calculate = wx.Button(panel, label="Calcular")
        btn_reset = wx.Button(panel, label="Reiniciar")
        btn_exit = wx.Button(panel, label="Sair")
        hbox4.Add(btn_calculate, flag=wx.RIGHT, border=10)
        hbox4.Add(btn_reset, flag=wx.RIGHT, border=10)
        hbox4.Add(btn_exit, flag=wx.RIGHT, border=10)
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        # Bind dos botões
        btn_calculate.Bind(wx.EVT_BUTTON, self.OnCalculate)
        btn_reset.Bind(wx.EVT_BUTTON, self.OnReset)
        btn_exit.Bind(wx.EVT_BUTTON, self.OnExit)

        # Lista dos valores
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.list_ctrl.InsertColumn(0, "ID", width=50)
        self.list_ctrl.InsertColumn(1, "Nome", width=150)
        self.list_ctrl.InsertColumn(2, "Endereço", width=200)
        self.list_ctrl.InsertColumn(3, "Altura (cm)", width=100)
        self.list_ctrl.InsertColumn(4, "Peso (Kg)", width=100)
        self.list_ctrl.InsertColumn(5, "IMC", width=100)
        vbox.Add(self.list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.SetSize((800, 400))
        self.Centre()

    def ConnectDatabase(self):
        #Conecto na base de dados e setando cursor
        self.conn = sqlite3.connect('imc.db')
        self.cursor = self.conn.cursor()

    def LoadData(self, nome):
        # Importando os dados da tabela
        self.list_ctrl.DeleteAllItems()  # Limpa a tabela antes de recarregar
        self.cursor.execute("SELECT * FROM imc WHERE nome = ?", (nome,))
        for row in self.cursor.fetchall():
            self.list_ctrl.Append(row)

    def OnCalculate(self, event):
        try:
            nome = self.txt_name.GetValue()
            endereco = self.txt_address.GetValue()
            height = float(self.txt_height.GetValue()) / 100
            weight = float(self.txt_weight.GetValue())
            bmi = weight / (height * height)
            self.result.SetLabel("IMC: {:.2f}".format(bmi))

            self.cursor.execute("""
                            INSERT INTO imc (nome, endereco, altura, peso, resultado)
                            VALUES (?, ?, ?, ?, ?)
                        """, (nome, endereco, height, weight, bmi))
            self.conn.commit()
            self.LoadData(nome)

        except ValueError:
            self.result.SetLabel("Erro: valores inválidos")

    def OnReset(self, event):
        self.txt_name.Clear()
        self.txt_address.Clear()
        self.txt_height.Clear()
        self.txt_weight.Clear()
        self.result.SetLabel("")
        self.list_ctrl.DeleteAllItems()
    def OnExit(self, event):
        self.Close()

def main():
    app = wx.App()
    frame = IMCCalculator(None)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()