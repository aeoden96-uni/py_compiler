from vepar import *


class T(TipoviTokena):
    FOR, COUT, ENDL, IF = 'for', 'cout', 'endl', 'if'
    OOTV, OZATV, VOTV, VZATV,UOTV,UZATV, TOČKAZ = '(){}[];'
    PLUSP, MMANJE = '++', '<<'
    NAVODNICI='"'

    #OPERATORI_PRIDRUZIVANJA
    PLUSJ,JEDNAKO = '+=','='

    

    #OPERATORI
    PLUS,PUTA,NA='+*^'

    #OPERATORI_USPOREDBE
    JJEDNAKO,MANJE = '==','<'
    #LOGICKI_OPERATORI
    AND,OR,NOT = 'and','or','not'



    #token za BREAK
    class BREAK(Token):
        literal = 'break'
        def izvrši(self, mem): raise Prekid


    #token za BOOL PRVA VARIJANTA 
    #class LOGVAR(Token):
    #    def vrijednost(self, mem): return int(self.sadržaj)

    class TRUE(Token):
        literal = 'TRUE'
        def vrijednost(self, mem, unutar): return 'TRUE'
        def izvrši(self, mem): return 'TRUE'

    class FALSE(Token):
        literal = 'FALSE'
        def vrijednost(self, mem, unutar): return 'FALSE'
        def izvrši(self, mem): return 'FALSE'

    class UNDEFINED(Token):
        literal = 'UNDEFINED'
        def vrijednost(self, mem, unutar): return 'UNDEFINED'
        def izvrši(self, mem): return 'UNDEFINED'

    
    #TOKENI ZA PRETVORBU TIPOVA
    class INT_TIP(Token):
        literal = 'int'

    class BOOL_TIP(Token):
        literal = 'bool'
    
    class STR_TIP(Token):
        literal = 'string'

    #token za BROJ
    class BROJ(Token):
        def vrijednost(self, mem): return int(self.sadržaj)
        def izvrši(self,mem):
            return int(self.sadržaj)


    
        
    #token za VARIJABLU
    class IME(Token):
        #vraća stogod je u memoriji na mjestu IME
        def vrijednost(self, mem): return mem[self]
        def vrsta(self): return 'IME'
        def izvrši(self,mem):
            return mem[self]

    class IME_LOG(Token):
        #vraća stogod je u memoriji na mjestu IME
        def vrijednost(self, mem): return mem[self]
        def vrsta(self): return 'IME_LOG'
        def izvrši(self,mem):
            return mem[self]

    class STRING(Token):
        #vraća stogod je u memoriji na mjestu IME
        def vrijednost(self): return self.sadržaj[1:-1]
        def izvrši(self,mem):
            #return mem[self]
            return self.sadržaj[1:-1]


    
    class U_OKOLINU(Token):
        def vrijednost(self, mem): 
            print("zatrazi vrij")
            return mem[self]

    class IZ_OKOLINE(Token):
        def vrijednost(self, mem): return mem[self]


def cpp(lex):
    for znak in lex:
        
        #zanemari prazan ZNAK, predi na iduci
        if znak.isspace(): lex.zanemari()

        #ako je trenutni plus
        elif znak == '+':
            #ako je i iduci '+' procitaj ga i sve strpaj u PLUSP
            if lex >= '+': yield lex.token(T.PLUSP)
            #ako je i iduci '=' procitaj ga i sve strpaj u PLUSP
            elif lex >= '=': yield lex.token(T.PLUSJ)
            
            #raisea LeksičkaGreška s porukom
            #else: raise lex.greška('u ovom jeziku nema samostalnog +')
            else: yield lex.token(T.PLUS)


        #ako je trenutni < i iduci < strpaj u MMANJE inace strpaj samo < u MANJE
        elif znak == '<': yield lex.token(T.MMANJE if lex >= '<' else T.MANJE)
        #slicno kao gore
        elif znak=='=': yield lex.token(T.JJEDNAKO if lex >= '=' else T.JEDNAKO)
        
        elif znak=='#':
            lex.zvijezda(identifikator)
            yield lex.literal(T.U_OKOLINU)

        elif znak=='$':
            lex.zvijezda(identifikator)
            yield lex.literal(T.IZ_OKOLINE)
        
        elif znak== '"':
            
            #lex.pročitaj_do(T.NAVODNICI)
            lex.zvijezda(identifikator)
            lex >> '"'
            yield lex.token(T.STRING)

        elif znak.isalpha() and znak.isupper():
            lex.zvijezda(identifikator)
            yield lex.literal(T.IME_LOG)
        elif znak.isalpha():
            lex.zvijezda(identifikator)
            yield lex.literal(T.IME)

        elif znak.isdecimal():
            lex.prirodni_broj(znak)
            yield lex.token(T.BROJ)

        else: yield lex.literal(T)

#DONE
#####################################################################

class P(Parser):
    lexer = cpp

    def start(self):
        VISE_NAREDBI = [self.naredba()]
        while not self > KRAJ: VISE_NAREDBI.append(self.naredba())
        return Program(VISE_NAREDBI)

    def naredba(self):
        if self > T.FOR: return self.petlja()
        elif self > T.IF: return self.grananje()
        elif self > T.IME: return self.pridruzivanje()
        elif self > T.IME_LOG: return self.pridruzivanje()
        elif self > T.U_OKOLINU: return self.u_okolinu()
        elif br := self >> T.BREAK:
            self >> T.TOČKAZ
            return br

    def petlja(self):
        kriva_varijabla = SemantičkaGreška(
            'Sva tri dijela for-petlje moraju imati istu varijablu.')
        self >> T.FOR, self >> T.OOTV
        i = self >> T.IME
        self >> T.JEDNAKO
        početak = self >> T.BROJ
        self >> T.TOČKAZ

        if (self >> T.IME) != i: raise kriva_varijabla
        self >> T.MANJE
        granica = self >> T.BROJ
        self >> T.TOČKAZ

        if (self >> T.IME) != i: raise kriva_varijabla
        if self >= T.PLUSP: inkrement = nenavedeno
        elif self >> T.PLUSJ: inkrement = self >> T.BROJ
        self >> T.OZATV

        if self >= T.VOTV:
            blok = []
            while not self >= T.VZATV: blok.append(self.naredba())
        else: blok = [self.naredba()]
        return Petlja(i, početak, granica, inkrement, blok)
        

    def iz_okoline(self):
        fn=self >> T.IZ_OKOLINE
        self >> T.OOTV
        self >>T.OZATV
        #return fn

        return Iz_okoline([fn])
        
        
        
    def u_okolinu(self):
        funkcija = self >> T.U_OKOLINU
        self >> T.OOTV

        if self >= T.OZATV:
            self >> T.TOČKAZ
            return U_okolinu([funkcija])
        elif ime:= self >= T.IME:
            self >> T.OZATV
            self >> T.TOČKAZ
            return U_okolinu([funkcija,ime])

        elif ime:= self >= T.IME_LOG:
            self >> T.OZATV
            self >> T.TOČKAZ
            return U_okolinu([funkcija,ime])
        else:
            izraz = self.izraz()
            self >> T.OZATV
            self >> T.TOČKAZ
            return U_okolinu([funkcija, izraz])
        

       

    #OK
    def grananje(self):
        self >> T.IF, self >> T.OOTV
        logika = self.logika()
        self >> T.OZATV

        return Grananje(logika, self.naredba())

    def pridruzivanje(self):
        if lijevo := self >= T.IME:
            self >> T.JEDNAKO
            izraz=self.izraz()
            self >> T.TOČKAZ
            return Pridruzivanje(lijevo,izraz)
        else:
            lijevo = self >> T.IME_LOG
            self >> T.JEDNAKO
            logika=self.logika()
            self >> T.TOČKAZ
            return Pridruzivanje(lijevo,logika)


    def logika(self):
        prvi = self.konj()

        if self >= T.OR:
            drugi =self.logika()
            return OR([prvi, drugi])
        else:
            return prvi

    def konj(self):
        log_literal = self.log_literal()
        if self >= T.AND: 
            drugi=self.konj()
            return AND([log_literal, drugi])
        else: 
            return log_literal

    def log_literal(self):
        if self >= T.OOTV:
            logika= self.ligika()
            self >> T.OZATV
            return logika
        elif var := self >= T.TRUE:
            return var
        elif var := self >= T.FALSE:
            return var
        elif var := self >= T.UNDEFINED:
            return var
        elif var := self >= T.IME_LOG:
            return var
        else:
            izraz1= self.izraz()
            if self >= T.MANJE:
                izraz2=self.izraz()
                return LESS([izraz1, izraz2])

            else:
                self >> T.JJEDNAKO
                izraz2=self.izraz()
                return EQ([izraz1, izraz2])


        

    def izraz(self):
        prvi = self.član()
        
        if self >= T.PLUS:
            drugi = self.izraz()
            return Zbroj([prvi, drugi])
        else:
            return prvi

    def član(self):
        faktor = self.faktor()
        if self >= T.PUTA: return Umnožak([faktor, self.član()])
        else: return faktor

    def faktor(self):
        baza = self.baza()
        if self >= T.NA: return Potencija(baza, self.faktor())
        else: return baza

    def baza(self):
        if broj := self >= T.BROJ: return broj
        if string := self >= T.STRING:
            return string

        elif self > T.IZ_OKOLINE:
            return self.iz_okoline()

        elif ime:= self >= T.IME:
            return ime
        
            
        elif log := self >= T.TRUE:
             return log
        elif log := self >= T.FALSE:
             return log
        elif log := self >= T.UNDEFINED:
             return log




        elif self >> T.OOTV: #PROMJENA TIPA
            if tip :=self >= T.INT_TIP:
                self >> T.OZATV
                u_zagradi=self.izraz()
                return U_int(u_zagradi)
            else:
                u_zagradi = self.izraz()
                self >> T.OZATV
                return u_zagradi

class Prekid(NelokalnaKontrolaToka): """Signal koji šalje naredba break."""



#DONE
#####################################################################


class Program(AST('naredbe')):
    def izvrši(self):
        mem = Memorija()
        try:  # break izvan petlje je zapravo sintaksna greška - kompliciranije
            for naredba in self.naredbe: naredba.izvrši(mem)
        except Prekid: raise SemantičkaGreška('nedozvoljen break izvan petlje')

class Petlja(AST('varijabla početak granica inkrement blok')):
    def izvrši(self, mem):
        kv = self.varijabla  # kontrolna varijabla petlje
        mem[kv] = self.početak.vrijednost(mem)
        while mem[kv] < self.granica.vrijednost(mem):
            try:
                for naredba in self.blok: naredba.izvrši(mem)
            except Prekid: break
            inkr = self.inkrement
            if inkr is nenavedeno: inkr = 1
            else: inkr = inkr.vrijednost(mem)
            mem[kv] += inkr 

class U_okolinu(AST('funkcija_logika')):
    def izvrši(self, mem):
        r=self.funkcija_logika[1].izvrši(mem)

        print("U OKOLINU POSLANO: "+ str(r))

        #for var in self.varijable: 
        #    print(var.vrijednost(mem), end=' ')
        #if self.novired ^ T.ENDL:
        #     print()

class U_int(AST('izraz')):
    def izvrši(self, mem):
        r=self.izraz.izvrši(mem)

        print(r)

        return int(r)

class Grananje(AST('logika naredba')):
    def izvrši(self, mem):
        if self.logika.vrijednost(mem) == T.TRUE:
            self.naredba.izvrši(mem)

class Pridruzivanje(AST('varijabla izraz')):
    def izvrši(self, mem):
        r=self.izraz.izvrši(mem)

        if self.varijabla.vrsta()=='IME':
            if r in [T.TRUE._name_, T.FALSE._name_,T.UNDEFINED._name_]:
                raise GreškaIzvođenja("Can't save logic value in a regular variable.")
            
        mem[self.varijabla] =r


class Iz_okoline(AST('funkcija_logika')):
    def izvrši(self, mem):
        print("IZ OKOLINE DOBIVENO: 11")
        return 11

class Zbroj(AST('pribrojnici')):
    def vrijednost(izraz):
        a, b = self.izraz.pribrojnici
        return a.vrijednost() + b.vrijednost()

    def optim(izraz):
        a, b = izraz.pribrojnici
        a, b = a.optim(), b.optim()
        if a == nula: return b
        elif b == nula: return a
        else: return Zbroj([a, b])

    def prevedi(izraz):
        for pribrojnik in izraz.pribrojnici: yield from pribrojnik.prevedi()
        yield ['ADD']
    
    def izvrši(self,mem):
        a=self.pribrojnici[0].izvrši(mem)
        b=self.pribrojnici[1].izvrši(mem)
        return a+b

class LESS(AST('izrazi')):
    def izvrši(self, mem):
        return
class EQ(AST('izrazi')):
    def izvrši(self, mem):
        return

class OR(AST('elements')):
    def izvrši(self, mem):
        if self.elements[0] or  self.elements[1] :
            return T.TRUE
class AND(AST('faktori')):
    def izvrši(self, mem):
        return

class Umnožak(AST('faktori')):
    def izvrši(self,mem):
        a=self.faktori[0].izvrši(mem)
        b=self.faktori[1].izvrši(mem)
        #return a*b
        return self.faktori[0].vrijednost(mem)*self.faktori[1].vrijednost(mem)

class Potencija(AST('baza eksponent')):
    def izvrši(self,mem):
        return self.baza.vrijednost(mem)**self.eksponent.vrijednost(mem)


######################################

ulaz ='''\

v=2 + $getTemp() ;

z=5;
Z = FALSE or TRUE;


#ispisi(Z);




'''
#print(ulaz)
P.tokeniziraj(ulaz)
######################################

cpp = P(ulaz)

#prikaz(cpp)

cpp.izvrši()