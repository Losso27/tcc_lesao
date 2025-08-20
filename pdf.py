from fpdf import FPDF
import utils

dict_etinia  = {13: "Amarelo", 14: "Branco", 15: "Indígena", 16: "Pardo", 17: "Preto"}
dict_condicoes = {28: "Trombose Venosa Profunda", 29:"Linfedema", 30:"Celulite Infecciosa", 31:"Erisipela", 32:"Lipodermatoesclerose", 33:"Fungos", 34:"Artrite", 35:"Osteomielite"}
dict_comorbidade = {5: "Hipertensão", 6: "Doença Arterial Obstrutiva Periférica", 7:"Varizes", 8:"Obesidade", 9:"Diabetes", 10:"Cardiopatia", 11:"Insuficiência Venosa Crônica", 12:"Hiperlipidemia"}
dict_doppler = {36: "Refluxo valvar", 37:"Fluxo Normal", 38:"Suspeita de Trombose", 39:"Insuficiência Venosa Crônica", 40:"Isquemia aguda", 41:"Doença Arterial oclusiva"}
dict_estilo_vida = {1:"Sedentário", 2: "Mobilidade Reduzida", 3: "Permanece sentado ou em pé durante muito tempo", 4: "Tabagismo"}
dict_exsudato = {24: "Seroso", 25: "Purulento", 26:"Sanguinolento", 27:"Sero-sanguinolento"}

class CustomPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, "Prontuario", border=1, ln=True, align="C")
        self.ln(5)
    

def create_pdf(data):

    aspecto_pele = data["aspecto_pele"].title()             
    aspecto_unha = data["aspecto_unha"].title()            
    bordas = data["bordas"].title()                    
    claudicacao = data["claudicacao"].title()
    condicoes_clinicas_associadas = translator(data["condicoes_clinicas_associadas"], dict_condicoes)
    comorbidade = translator(data["comorbidade"], dict_comorbidade)                  
    doppler = translator(data["doppler"], dict_doppler)                     
    dor = utils.convert_string_to_float(data["dor"])                          
    dor_em_elevacao = data['dor_em_elevacao'].title()             
    edema = data["edema"]
    estilo_de_vida = translator(data["estilo_de_vida"], dict_estilo_vida)
    etnia = translator(data["etnia"], dict_etinia)         
    enchimento_capilar = data["enchimento_capilar"].title()         
    exsudato = translator([data["exsudato"]], dict_exsudato)                   
    exsudato_volume = utils.convert_string_to_float(data["exsudato_volume"])            
    idade = utils.convert_string_to_age(data["data_nascimento"])
    itb = utils.convert_string_to_float(data["itb"])                     
    localizacao = data["localizacao"].title()             
    pilificacao = data["pilificacao"].title()            
    profundidade = data ["profundidade"].title()
    pulso = data["pulso"].title()                               
    sexo = data["sexo"].title()                        
    tamanho_lesao = utils.convert_string_to_float(data["tamanho_lesao"])               
    temperatura = data["temperatura"].title()
    tipo = data["tipo"]
    risco = data["risco"]
    nome = data["nome"].title()
    
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
    pdf.cell(half_width, 10, f"Dimensão da Lesão: {tamanho_lesao}cm²", border=1, ln=True)

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
    pdf.cell(half_width, 10, f"Cladicação: {claudicacao}", border=1, ln=True)

    pdf.multi_cell(page_width, 10, f"Comorbidades: {comorbidade}", border=1)
    pdf.ln(0)

    # Row 8 (optional: pilificacao and enchimento capilar)
    pdf.cell(half_width, 10, f"ITB: {itb}", border=1)
    pdf.cell(half_width, 10, f"Enchimento Capilar: {enchimento_capilar}", border=1, ln=True)

    # Row 11 (optional: doppler and ITB)
    pdf.multi_cell(page_width, 10, f"Doppler: {doppler}", border=1)
    
    

    return pdf.output()

def translator(source, dict):
    output = ""
    for i in source:
        output += dict[i] + ", "
    return output[:-2]

