from vepar import *
import turtle
from time import sleep
from inspect import signature


class T(TipoviTokena):
    FOR, COUT, ENDL, IF,IN = 'for', 'cout', 'endl', 'if','in'
    OOTV, OZATV, VOTV, VZATV,UOTV,UZATV,POTV,PZATV ,TOČKAZ = '(){}[]<>;'
    PLUSP, MMANJE = '++', '<<'
    NAVODNICI='"'
    ZAREZ= ','
    #OPERATORI_PRIDRUZIVANJA
    PLUSJ,JEDNAKO = '+=','='

    

    #OPERATORI
    PLUS,PUTA,NA,MINUS,DJELJENO='+*^-/'

    #OPERATORI_USPOREDBE
    JJEDNAKO,MANJE = '==','<'
    #LOGICKI_OPERATORI
    AND,OR,NOT = 'and','or','not'



    


    def getBool(integer):
        if integer == 1:
            return T.TRUE
        elif integer == -1:
            return T.FALSE 
        elif integer == 0:
            return T.UNDEFINED
        else:
            raise SintaksnaGreška("")

    class TRUE(Token):
        literal = 'TRUE'
        def vrijednost(self, mem): return 1
        def izvrši(self,mem): return self

    class FALSE(Token):
        literal = 'FALSE'
        def vrijednost(self, mem): return -1
        def izvrši(self,mem): return self

    class UNDEFINED(Token):
        literal = 'UNDEFINED'
        def vrijednost(self, mem): return 0
        def izvrši(self,mem): return self

    
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
            return self


    
        
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

    class IME_LISTA(Token):
        #vraća stogod je u memoriji na mjestu IME
        def vrijednost(self, mem): return mem[self]
        def vrsta(self): return 'IME_LISTA'
        def izvrši(self,mem):
            return mem[self]

    class STRING(Token):
        #vraća stogod je u memoriji na mjestu IME
        def vrijednost(self,mem): return self.sadržaj[1:-1]
        def izvrši(self,mem):
            #return mem[self]
            return self



    #token za BREAK
    class BREAK(Token):
        literal = 'break'
        def izvrši(self, mem): raise Prekid
        def vrijednost(self, mem): raise Prekid


    #FJE KOJE DOLAZE IZ OKOLINE POCINJU S $
    class IZ_OKOLINE_ORI(Token):
        #get distance from the wall
        literal = 'getOrientation'
        def izvrši(self, mem): return mem[self]
        def vrijednost(self, mem): return mem[self]
    
    class IZ_OKOLINE_COORD(Token):
        #get distance from the wall
        literal = 'getCoord'
        def izvrši(self, mem): return mem[self]
        def vrijednost(self, mem): return mem[self]
    
    


    

    
    #FJE KOJE IDU U OKOLINU POCINJU S #
    class U_OKOLINU_STEPS(Token):
        literal = 'setSteps'
        def vrijednost(self, mem): 
            return mem[self]
        def vrijednost(self, mem): return mem[self]

    class U_OKOLINU_POWER(Token):
        literal = 'setPower'
        def vrijednost(self, mem): 
            return mem[self]
        def vrijednost(self, mem): return mem[self]
    class U_OKOLINU_SPEED(Token):
        literal = 'setSpeed'
        def vrijednost(self, mem): 
            return mem[self]
        def vrijednost(self, mem): return mem[self]
    class U_OKOLINU_PRINT(Token):
        literal = 'print'
        def vrijednost(self, mem): 
            return mem[self]
        def vrijednost(self, mem): return mem[self]
    class U_OKOLINU_ROTATION(Token):
        literal = 'setRot'
        def vrijednost(self, mem): 
            return mem[self]
        def vrijednost(self, mem): return mem[self]


    


def cpp(lex):
    for znak in lex:
        
        if znak.isspace(): lex.zanemari()

        elif znak == '+':
            if lex >= '+': yield lex.token(T.PLUSP)
            elif lex >= '=': yield lex.token(T.PLUSJ)
            else: yield lex.token(T.PLUS)
      
        elif znak == '<': yield lex.token(T.MMANJE if lex >= '<' else T.MANJE)
        elif znak=='=': yield lex.token(T.JJEDNAKO if lex >= '=' else T.JEDNAKO)
        
        #PREPOZNAJE "neki string"
        elif znak== '"':
            lex.pročitaj_do('"')
            yield lex.token(T.STRING)

        #PREPOZNAJE LISTNU VARIJABLU (pocinje Velikim slovom L) 
        elif znak == 'L':
            lex.zvijezda(identifikator)
            yield lex.literal(T.IME_LISTA)

        #PREPOZNAJE LOGICKU VARIJABLU (pocinje Velikim slovom) 
        elif znak.isalpha() and znak.isupper():
            lex.zvijezda(identifikator)
            yield lex.literal(T.IME_LOG)

        #PREPOZNAJE OBICNU VARIJABLU     
        elif znak.isalpha():
            lex.zvijezda(identifikator)
            yield lex.literal(T.IME)

        #PREPOZNAJE BROJ
        elif znak.isdecimal():
            lex.prirodni_broj(znak)
            yield lex.token(T.BROJ)

        #PREPOZNAJE JEDNOLINIJSKI KOMENTAR
        elif znak == '/':
            if lex  >= '/':
                lex.pročitaj_do('\n')
                lex.zanemari()
                
        else: yield lex.literal(T)


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
        elif self > {T.IME,T.IME_LOG,T.IME_LISTA}: 
            return self.pridruzivanje()
        elif self > {T.U_OKOLINU_PRINT, T.U_OKOLINU_SPEED,T.U_OKOLINU_STEPS,T.U_OKOLINU_POWER,T.U_OKOLINU_ROTATION}: 
            return self.u_okolinu()
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
        fn=self >> {T.IZ_OKOLINE_COORD,T.IZ_OKOLINE_ORI}
        self >> T.OOTV
        self >>T.OZATV

        return Iz_okoline(fn)
        
        
        
    def u_okolinu(self):
        #definira sto moze biti argumenti fja koje idu u okolinu

        f = self >> {T.U_OKOLINU_PRINT,T.U_OKOLINU_STEPS,T.U_OKOLINU_SPEED,T.U_OKOLINU_POWER,T.U_OKOLINU_ROTATION}

        self >> T.OOTV

        if f ^ T.U_OKOLINU_POWER:
            logika = self.logika()
            self >> T.OZATV
            self >> T.TOČKAZ
            return U_okolinu([f,logika])
            
        
        else:
            izraz = self.izraz()
            self >> T.OZATV
            self >> T.TOČKAZ
            return U_okolinu([f,izraz])

    
    def grananje(self):
        self >> T.IF, self >> T.OOTV
        logika = self.logika()
        self >> T.OZATV

        return Grananje(logika, self.naredba())

    def pridruzivanje(self):
        if lijevo := self >= T.IME:
            #ako je obicno pridruzivanje
            if self >= T.JEDNAKO:
                izraz=self.izraz()
                self >> T.TOČKAZ
                return Pridruzivanje(lijevo,izraz)

            #ako je pridruzivanje oblika var,...var= lista
            else:
                el = [lijevo]
                while self>=T.ZAREZ: 
                    novi= self >>  T.IME
                    el.append(novi)
                self >> T.JEDNAKO
                if  self > T.IZ_OKOLINE_COORD:
                    tip ='okolina'
                    value= self.iz_okoline()
                elif ime := self >= T.IME_LISTA:
                    tip='ime'
                    value=ime
                else:
                    tip='lista'
                    value=self.lista()
                self >> T.TOČKAZ
                return Pridruzivanje_liste(el,tip,value)

        elif lijevo := self >= T.IME_LOG:
            self >> T.JEDNAKO
            logika=self.logika()
            self >> T.TOČKAZ
            return Pridruzivanje(lijevo,logika)
        elif lijevo :=  self >> T.IME_LISTA:
            self >> T.JEDNAKO
            lista=self.lista()
            self >> T.TOČKAZ
            return Pridruzivanje(lijevo,lista)
        else:
            pass
            

    def lista(self):
        if self >= T.UOTV:
            if self >= T.UZATV: return Lista([])
            el = [self.lista()]
            while self>=T.ZAREZ and not self>T.UZATV: el.append(self.lista())
            self >> T.UZATV
            return Lista(el)
        else: 
            
            #return self >> {T.BROJ}
            return self.izraz()
    

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
            #ako je upis pocinje s  '(BOOL)...'
            if self >= T.BOOL_TIP:
                self >> T.OZATV
                izraz= self.izraz()
                return U_bool(izraz)

            #ako je upis pocinje s '(..logika...)    
            logika= self.logika()
            self >> T.OZATV
            return logika

        #ako je literal T,U,F
        elif var := self >= {T.TRUE,T.FALSE,T.UNDEFINED,T.IME_LOG}:
            return var


        elif self >= T.NOT:
            #NOT
            
            #Ako iza not nije zagrada
            if drugi :=self >= {T.IME_LOG,T.TRUE,T.FALSE,T.UNDEFINED}:
                return NOT(drugi)

            #ako je zagrada
            else:
                self >> T.OOTV
                u_zagradi = self.logika()
                self >> T.OZATV
                return NOT(logika)

        else:
            #jedino preostaje ako literal pocinje s izrazom
            izraz1= self.izraz()
            if self >= T.JJEDNAKO:
                izraz2=self.izraz()
                return EQ([izraz1, izraz2])
            elif self >= T.MANJE:
                izraz2=self.izraz()
                return LESS([izraz1, izraz2])
            elif self >= T.IN:
                if lista := self >= T.IME_LISTA:
                    pass
                else:
                    lista=self.lista()
                return In(izraz1,lista)
   

    def izraz(self):
        

        prvi = self.član()
        
        if self >= T.PLUS:
            drugi = self.izraz()
            return Zbroj([prvi, drugi])
        elif self >= T.MINUS:
            drugi = self.izraz()
            return Minus([prvi, drugi])
        else:
            return prvi

    def član(self):
        faktor = self.faktor()
        if self >= T.PUTA: return Umnožak([faktor, self.član()])
        elif self >= T.DJELJENO: return Količnik([faktor, self.član()])
        else: return faktor

    def faktor(self):
        baza = self.baza()
        if self >= T.NA: return Potencija(baza, self.faktor())
        else: return baza

    def baza(self):
        if broj := self >= T.BROJ: return broj
        if string := self >= T.STRING: return string

        #ako se tu nalazi neka fja. koja nesto vraca iz okoline
        elif self > {T.IZ_OKOLINE_ORI,T.IZ_OKOLINE_COORD}:
            return self.iz_okoline()

        elif ime:= self >= T.IME:
            return ime
        #ako se nalazi ime liste, onda dohvati na mjestu 'izraz' vrijednost tj. listVar[izraz]
        elif ime_liste:= self >= T.IME_LISTA:
            self >> T.UOTV
            izraz=self.izraz()
            self >> T.UZATV
            return Dohvat_liste(ime_liste,izraz)
        
            
        elif log := self >= T.TRUE:
             return log
        elif log := self >= T.FALSE:
             return log
        elif log := self >= T.UNDEFINED:
             return log

        if self >= T.MINUS:
            #UNARNI MINUS

            if drugi :=self >= {T.IME,T.BROJ}:
                return Minus([0, drugi])
            else:
                self >> T.OOTV
                u_zagradi = self.izraz()
                self >> T.OZATV
                return Minus([0, u_zagradi])


        elif self >> T.OOTV: 
            #ako je iduci token '(' , jedino moze biti promjena tipa ili '(izraz)'
            
            if tip :=self >= T.INT_TIP:
                #PROMJENA TIPA U int
                self >> T.OZATV
                if drugi :=self >= {T.IME,T.BROJ,T.STRING}:
                    return U_int(drugi)
                else:
                    self >> T.OOTV
                    u_zagradi = self.izraz()
                    self >> T.OZATV
                    return U_int(u_zagradi)
    
            elif tip :=self >= T.STR_TIP:
                #PROMJENA TIPA U string
                self >> T.OZATV
                if drugi :=self >= {T.IME,T.BROJ,T.STRING}:
                    return U_string(drugi)
                else:
                    self >> T.OOTV
                    u_zagradi = self.izraz()
                    self >> T.OZATV
                    return U_string(u_zagradi)

            
            else: 
                #u zagradi
                u_zagradi = self.izraz()
                self >> T.OZATV
                return u_zagradi


class Prekid(NelokalnaKontrolaToka): """Signal koji šalje naredba break."""



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

class Lista(AST('elementi')):
    def vrijednost(self,mem): 
        print("u vrijednosti od Lista")
        return [el.vrijednost() for el in self.elementi]

class U_int(AST('izraz')):
    def izvrši(self, mem):
        r=self.izraz.vrijednost(mem)

        print(r)

        return int(r)
    def vrijednost(self,mem):
        r=self.izraz.vrijednost(mem)
        return int(r)

class U_string(AST('izraz')):
    def izvrši(self, mem):
        r=self.izraz.vrijednost(mem)
        print(r)
        return int(r)
    def vrijednost(self,mem):
        r=self.izraz.vrijednost(mem)
        return str(r)

class U_bool(AST('izraz')):
    def izvrši(self, mem):
        r=self.izraz.vrijednost(mem)
        print(r)
        return int(r)
    def vrijednost(self,mem):
        r=self.izraz.vrijednost(mem)
        if r=='UNDEFINED' or r==0: return 0
        elif r== 'TRUE' or r==1: return 1
        elif r =='FALSE' or r==-1: return -1
        return -1

class Grananje(AST('logika naredba')):
    def izvrši(self, mem):
        if self.logika.vrijednost(mem) == 1:
            #u troclanoj logici, TRUE je u pozadini 1
            return self.naredba.vrijednost(mem)


class Pridruzivanje_liste(AST('varijable tip lista')):
    def izvrši(self, mem):
       
       
        if self.tip == 'ime':
            #ako je s desne strane varijabla koja cuva listu
            l=self.lista.vrijednost(mem) 
            for (var,list_elm) in zip(self.varijable, l):
                mem[var] =list_elm.vrijednost(mem) 

        elif self.tip == 'okolina':
            l=self.lista.vrijednost(mem) 
            for (var,list_elm) in zip(self.varijable, l):
                mem[var] =list_elm
        elif self.tip == 'lista':
            # s desne strane je eksplicitna lista
            l=self.lista[0]
            for (var,list_elm) in zip(self.varijable, l):
                mem[var] =list_elm.vrijednost(mem) 
            

        
    def vrijednost(self, mem):
        #NE POKRECE SE
        pass



class Dohvat_liste(AST('ime_liste izraz')):
    def vrijednost(self, mem):
       
        l=self.ime_liste.vrijednost(mem) 
        i=self.izraz.vrijednost(mem) 
        return l[i].vrijednost(mem) 



class Pridruzivanje(AST('varijabla izraz')):
    def izvrši(self, mem):
        if self.varijabla.vrsta()=='IME_LISTA':
            r=self.izraz.elementi
        else:
            r=self.izraz.vrijednost(mem)
        
        if self.varijabla.vrsta()=='IME':
            if r in [T.TRUE._name_, T.FALSE._name_,T.UNDEFINED._name_]:
                raise GreškaIzvođenja("Can't save logic value in a regular variable.")

        mem[self.varijabla] =r
    def vrijednost(self, mem):
        r=self.izraz.vrijednost(mem)

        if self.varijabla.vrsta()=='IME':
            if r in [T.TRUE._name_, T.FALSE._name_,T.UNDEFINED._name_]:
                raise GreškaIzvođenja("Can't save logic value in a regular variable.")

        mem[self.varijabla] =r

class U_okolinu(AST('funkcija_logika')):
    def izvrši(self, mem):
        self.vrijednost(mem)
        #r=self.funkcija_logika[1].vrijednost(mem)



    def vrijednost(self, mem):
        r=self.funkcija_logika[1].vrijednost(mem)
        if self.funkcija_logika[0] ^ T.U_OKOLINU_POWER:
            print("U okolinu dan power: " + str(r))
            #sleep(2)
            if r == -1:
                t.penup()
            elif r== 1 :
                t.pendown()
            return r
        
        elif self.funkcija_logika[0] ^ T.U_OKOLINU_PRINT:
            print("Ispisujem: " + str(r))
            return r
        elif self.funkcija_logika[0] ^ T.U_OKOLINU_ROTATION:
            print("U okolinu postavljen rotation: " + str(r))
            t.left(r)
            return r
        elif self.funkcija_logika[0] ^ T.U_OKOLINU_SPEED:
            print("U okolinu postavljen speed: " + str(r))
            t.pen(speed=r)
            return r
        elif self.funkcija_logika[0] ^ T.U_OKOLINU_STEPS:
            print("U okolinu postavljen broj koraka: " + str(r))
            
            t.forward(r)
            return r
        else:
            raise GreškaIzvođenja("iz okoline nema")

class Iz_okoline(AST('funkcija_logika')):
    def izvrši(self, mem):
        print("IZ OKOLINE DOBIVENO: 11")
        return 11
    def vrijednost(self, mem):
      
       
        if self.funkcija_logika ^ T.IZ_OKOLINE_ORI:
            print(f"IZ OKOLINE DOBIVENA orijentacija: {int(t.heading())}")
            return int(t.heading())
        elif self.funkcija_logika ^ T.IZ_OKOLINE_COORD:
            print("IZ OKOLINE DOBIVENE koordinate: " + str(t.pos()))
            return [int(t.pos()[0]),int(t.pos()[1])]
        else:
            raise GreškaIzvođenja("iz okoline nema")

class LESS(AST('izrazi')):
    def vrijednost(self,mem):
        a=self.izrazi[0].vrijednost(mem)
        b=self.izrazi[1].vrijednost(mem)

        return a < b

class EQ(AST('izrazi')):
    def izvrši(self, mem):
        a=self.izrazi[0].izvrši(mem)
        b=self.izrazi[1].izvrši(mem)

    def vrijednost(self,mem):
        a=self.izrazi[0].vrijednost(mem)
        b=self.izrazi[1].vrijednost(mem)

        return a==b
           
class In(AST('izraz lista')):
    def vrijednost(self,mem):
        a=self.izraz.vrijednost(mem)

        if self.lista ^ T.IME_LISTA:
            l=self.lista.vrijednost(mem)
        else:
            l=self.lista[0]

      
        for i in l:
            if a == i.vrijednost(mem):
                return 1
        return -1
        

       
class OR(AST('literali')):
    #OR(A, B) === MAX(A, B)
    def izvrši(self, mem):
       
        a=self.literali[0].vrijednost(mem)
        b=self.literali[1].vrijednost(mem)

        val= max(a,b)
        #u troclanoj logici, OR je u pozadini max(a,b)
        return val
        return a if a.vrijednost(mem) > b.vrijednost(mem) else b

    def vrijednost(self, mem):
           
        a=self.literali[0].vrijednost(mem)
        b=self.literali[1].vrijednost(mem)

        val= max(a,b)
        return val
        return a if a.vrijednost(mem) > b.vrijednost(mem) else b
                     
class AND(AST('literali')):
    #AND(A, B) ===MIN(A, B)
    def izvrši(self, mem):

        pass
        
        return a if a.vrijednost(mem) < b.vrijednost(mem) else b
    def vrijednost(self,mem):
        a=self.literali[0].vrijednost(mem)
        b=self.literali[1].vrijednost(mem)

        val= min(a,b)
        #u troclanoj logici, AND je u pozadini min(a,b)
        return val

class NOT(AST('literal')):
    #NOT(A) === -A
    def vrijednost(self, mem):
        a=self.literal.vrijednost(mem)
        return -a

class Zbroj(AST('pribrojnici')):
    def vrijednost(self,mem):
        a, b = self.pribrojnici
        return a.vrijednost(mem) + b.vrijednost(mem)

    def optim(self,izraz):
        a, b = izraz.pribrojnici
        a, b = a.optim(), b.optim()
        if a == nula: return b
        elif b == nula: return a
        else: return Zbroj([a, b])

    def prevedi(self,izraz):
        for pribrojnik in izraz.pribrojnici: yield from pribrojnik.prevedi()
        yield ['ADD']
    
    def izvrši(self,mem):
        a=self.pribrojnici[0].izvrši(mem)
        b=self.pribrojnici[1].izvrši(mem)
        return a+b

class Umnožak(AST('faktori')):
    def izvrši(self,mem):
        a=self.faktori[0].izvrši(mem)
        b=self.faktori[1].izvrši(mem)
        return a*b

    def optim(self,izraz):
        a, b = izraz.faktori
        a, b = a.optim(), b.optim()
        if a == jedan: return b
        elif b == jedan: return a
        elif nula in {a, b}: return nula
        else: return Umnožak([a, b])

    def prevedi(self,izraz):
        for faktor in izraz.faktori: yield from faktor.prevedi()
        yield ['MUL']

    def vrijednost(self,mem):
        a=self.faktori[0].vrijednost(mem)
        b=self.faktori[1].vrijednost(mem)
        return a*b

class Minus(AST('pribrojnici')):
    def vrijednost(self,mem):
        a, b = self.pribrojnici
        if a != 0:
            return a.vrijednost(mem) - b.vrijednost(mem)
        else:
            #unarni minus
            return  - b.vrijednost(mem)

    def optim(self,izraz):
        a, b = izraz.pribrojnici
        a, b = a.optim(), b.optim()
        if a == nula: return -b               # ?
        elif b == nula: return a
        else: return Minus([a, b])

    def prevedi(self,izraz):
        for pribrojnik in izraz.pribrojnici: yield from pribrojnik.prevedi()
        yield ['SUB']                         # ?
    
    def izvrši(self,mem):
        a=self.pribrojnici[0].izvrši(mem)
        b=self.pribrojnici[1].izvrši(mem)
        return a-b

class Količnik(AST('faktori')):
    def izvrši(self,mem):
        a=self.faktori[0].izvrši(mem)
        b=self.faktori[1].izvrši(mem)
        return a/b

    def optim(self,izraz):
        a, b = izraz.faktori
        a, b = a.optim(), b.optim()
        if a == nula: return nula
        elif b == jedan: return a
        else: return Količnik([a, b])

    def prevedi(self,izraz):
        for faktor in izraz.faktori: yield from faktor.prevedi()
        yield ['DIV']

    def vrijednost(self,mem):
        a=self.faktori[0].vrijednost(mem)
        b=self.faktori[1].vrijednost(mem)
        return a/b

class Potencija(AST('baza eksponent')):
    def izvrši(self,mem):
        a=self.baza.izvrši(mem)
        b=self.eksponent.izvrši(mem)
        return a**b
        

######################################



ulaz ='''\
print("program pocinje s radom");
rot = 90;
x,y= getCoord();
r=getOrientation();


setPower(TRUE);
setSpeed(2);

for (i=0; i < 8 ; i++){
    
    
    x,y= getCoord();
    r=getOrientation();

    setSteps(50);
    setRot(rot);

    if (i == 4) rot =  rot-45;
    if (i == 4) break;
}

print("program gotov s radom");

'''



print(ulaz)
P.tokeniziraj(ulaz)


######################################
#turtle grafika nam treba kod kompleksnijih primjera
# set***() funkcije  salju komande robotu
# get***() dobivaju  dobivaju komande iz okoline i spremaju se u var
######################################
def init_turtle(t):
    #inits the screen and walls
       
    t.penup()
    t.goto(-300,300)
    t.pen(pencolor="black", fillcolor="white", pensize=10, speed=9)
    t.begin_fill()


    t.pendown()
    for i in range(4):
        t.fd(600)
        t.rt(90)
    t.end_fill()
    #t.write("fan")
    t.penup()
    t.home()
    t.pendown()
    t.pen(pencolor="black", pensize=2, speed=1)

cpp = P(ulaz)

prikaz(cpp)

t = turtle.Turtle()

init_turtle(t)

cpp.izvrši()

t.getscreen()._root.mainloop()




