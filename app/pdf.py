from fpdf import FPDF

dict_etinia  = {13: "Amarelo", 14: "Branco", 15: "Indígena", 16: "Pardo", 17: "Preto"}
dict_condicoes = {28: "Trombose Venosa Profunda", 29:"Linfedema", 30:"Celulite Infecciosa", 31:"Erisipela", 32:"Lipodermatoesclerose", 33:"Fungos", 34:"Artrite", 35:"Osteomielite"}
dict_comorbidade = {5: "Hipertensão", 6: "Doença Arterial Obstrutiva Periférica", 7:"Varizes", 8:"Obesidade", 9:"Diabetes", 10:"Cardiopatia", 11:"Insuficiência Venosa Crônica", 12:"Hiperlipidemia"}
dict_doppler = {36: "Refluxo valvar", 37:"Fluxo Normal", 38:"Suspeita de Trombose", 39:"Insuficiência Venosa Crônica", 40:"Isquemia aguda", 41:"Doença Arterial oclusiva"}
dict_estilo_vida = {1:"Sedentário", 2: "Mobilidade Reduzida", 3: "Permanece sentado ou em pé durante muito tempo", 4: "Tabagismo"}
dict_exsudato = {24: "Seroso", 25: "Purulento", 26:"Sanguinolento", 27:"Sero-sanguinolento"}

class CustomPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, "Prontuário", border=1, ln=True, align="C")
        self.ln(5)
    

def create_pdf(data):

    paciente = data[0].to_dict()
    aspecto_pele = paciente["aspecto_pele"].title()             
    aspecto_unha = paciente["aspecto_unha"].title()            
    bordas = paciente["bordas"].title()                    
    claudicacao = translator_boolean(paciente["claudicacao"])
    condicoes_clinicas_associadas = translator(paciente["condicoes_clinicas_associadas"], dict_condicoes)
    comorbidade = translator(paciente["comorbidade"], dict_comorbidade)                  
    doppler = translator(paciente["doppler"], dict_doppler)                     
    dor = paciente["dor"].title()                          
    dor_em_elevacao = translator_boolean(paciente['dor_em_elevacao'])             
    edema = paciente["edema"]
    estilo_de_vida = translator(paciente["estilo_de_vida"], dict_estilo_vida)
    etnia = translator(paciente["etnia"], dict_etinia)         
    enchimento_capilar = paciente["enchimento_capilar"].title()         
    exsudato = translator([paciente["exsudato"]], dict_exsudato)                   
    exsudato_volume = paciente["exsudato_volume"].title()         
    idade = paciente["idade"]
    itb = paciente["itb"]                   
    localizacao = ",".join(paciente["localizacao"])          
    pilificacao = paciente["pilificacao"].title()            
    profundidade = paciente ["profundidade"].title()
    pulso = paciente["pulso"].title()                               
    sexo = paciente["sexo"].title()                        
    tamanho_lesao = paciente["comprimento_lesao"] * paciente["largura_lesao"]       
    temperatura = paciente["temperatura"].title()
    tipo = paciente["tipo"]
    risco = paciente["risco"]
    peso = paciente["peso"]
    altura = paciente["altura"]
    imc = peso / altura ** 2
    nome = paciente["nome"].title()

    if itb == None:
        itb = ""

    historico_tratamento = "Tratamento:\n"
    for p in data:
        p_dict = p.to_dict()
        data_exame = p_dict['data_exame']
        tratamento_terapia_topica = p_dict["tratamento_terapia_topica"]
        tratamento_cobertura = p_dict["tratamento_cobertura"]
        tratamento_remocao = p_dict["tratamento_remocao"]
        historico_tratamento += f"- {data_exame} Terapia tópica: {tratamento_terapia_topica} Cobertura Primária: {tratamento_cobertura} Remoção de Tecido:{tratamento_remocao} \n" 
    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Half-width for 2 columns (minus small spacing)
    page_width = pdf.w - 2 * pdf.l_margin
    half_width = page_width / 2

    pdf.set_font("Helvetica", "", 12)

    pdf.cell(half_width, 10, f"Nome: {nome}", border=1)
    pdf.cell(half_width, 10, f"Idade: {idade}", border=1, ln=True)

    pdf.cell(half_width, 10, f"Tipo da Lesão: {tipo}", border=1)
    pdf.cell(half_width, 10, f"Risco: {risco}", border=1, ln=True)

    pdf.cell(half_width, 10, f"Sexo: {sexo}", border=1,)
    pdf.cell(half_width, 10, f"Etnia: {etnia}", border=1, ln=True)
    

    # Row 1
    pdf.multi_cell(half_width * 2, 10, f"Localização da Lesão: {localizacao}", border=1)
    pdf.ln(0)

    pdf.cell(half_width, 10, f"Aspecto da pele: {aspecto_pele}", border=1)
    pdf.cell(half_width, 10, f"Dimensão da Lesão: {tamanho_lesao:.2f} cm²", border=1, ln=True)

    # Row 2
    pdf.cell(half_width, 10, f"Profundidade da Lesão: {profundidade}", border=1)
    pdf.cell(half_width, 10, f"Bordas da Lesão: {bordas}", border=1, ln=True)

    # Row 3
    pdf.cell(half_width, 10, f"Dor na elevação: {dor_em_elevacao}", border=1)
    pdf.cell(half_width, 10, f"Intensidade da dor {dor}", border=1, ln=True)

    # Row 4
    pdf.cell(half_width, 10, f"Aspecto Exsudato: {exsudato}", border=1)
    pdf.cell(half_width, 10, f"Volume Exsudato {exsudato_volume}", border=1, ln=True)

    # Row 5
    pdf.cell(half_width, 10, f"Edema: {edema}", border=1)
    pdf.cell(half_width, 10, f"Temperatura: {temperatura}", border=1, ln=True)

    pdf.multi_cell(page_width, 10, f"Estilo de Vida: {estilo_de_vida}", border=1)
    pdf.ln(0)

    pdf.cell(half_width, 10, f"Pulso: {pulso}", border=1)
    pdf.cell(half_width, 10, f"Aspecto Unhas: {aspecto_unha}", border=1, ln=True)

    pdf.multi_cell(page_width, 10, f"Condições Clínicas Associadas: {condicoes_clinicas_associadas}", border=1)
    pdf.ln(0)

    pdf.cell(half_width, 10, f"Pilificação: {pilificacao}", border=1)
    pdf.cell(half_width, 10, f"Claudicação: {claudicacao}", border=1, ln=True)

    pdf.multi_cell(page_width, 10, f"Comorbidades: {comorbidade}", border=1)
    pdf.ln(0)

    pdf.cell(half_width, 10, f"ITB: {itb}", border=1)
    pdf.cell(half_width, 10, f"Enchimento Capilar: {enchimento_capilar}", border=1, ln=True)

    pdf.multi_cell(page_width, 10, f"Doppler: {doppler}", border=1)
    pdf.ln(0)

    pdf.cell(half_width, 10, f"Peso: {peso:.1f} Kg", border=1)
    pdf.cell(half_width, 10, f"Altura: {altura:.2f} m", border=1, ln=True)

    pdf.multi_cell(page_width, 10, f"IMC: {imc:.2f} Kg/m² ({translator_imc(imc)})", border=1)
    pdf.ln(0)

    pdf.multi_cell(page_width, 10, f"Histórico Tratamento:")
    pdf.ln(0)
    for p in data:
        p_dict = p.to_dict()
        data_exame = p_dict['data_exame']
        tratamento_terapia_topica = p_dict["tratamento_terapia_topica"]
        tratamento_cobertura = p_dict["tratamento_cobertura"]
        tratamento_remocao = p_dict["tratamento_remocao"]
        pdf.multi_cell(page_width, 10, f"- {data_exame:%d/%m/%Y}\nTerapia tópica: {tratamento_terapia_topica} \nCobertura Primária: {tratamento_cobertura} \nRemoção de Tecido: {tratamento_remocao} \n")
        pdf.ln(0)


    return pdf.output()

def translator(source, dict):
    output = ""
    for i in source:
        if i != None:
            output += dict[i] + ", "
    return output[:-2]

def translator_boolean(source):
    if source:
        return "Sim"
    else:
        return "Não"

def translator_imc(imc):
    if imc < 18.5:
        return "Baixo Peso"
    elif imc >= 18.5 and imc < 25:
        return "Peso Normal"
    elif imc >= 25 and imc < 30:
        return "Pré-obesidade"
    elif imc >= 30 and imc < 35:
        return "Obesidade Grau I"
    elif imc >= 35 and imc < 40:
        return "Obesidade Grau II"
    elif imc >= 40:
        return "Obesidade Grau III"