from inlexer import Lexer
from class_parser import Parser
import time
import psutil

start_time = time.time()

codigo_pascal = """program test1;		{Este arquivo representa um programa correto}

var			{Existem diversos erros que podem ser gerados neste arquivo. Alguns exemplos:}
 
  a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx, yy, zz: integer;
  x, y, z, aa_real, bb_real, cc_real, dd_real, ee_real, ff_real, gg_real, hh_real, ii_real, jj_real, kk_real, ll_real, mm_real, nn_real, oo_real, pp_real, qq_real, rr_real, ss_real, tt_real, uu_real, vv_real, ww_real, xx_real, yy_real, zz_real: real;
  chave, chave2, chave3, chave4, chave5, chave6, chave7, chave8, chave9, chave10, chave11, chave12, chave13, chave14, chave15, chave16, chave17, chave18, chave19, chave20, chave21, chave22, chave23, chave24, chave25, chave26, chave27, chave28, chave29, chave30: boolean;

  procedure LimparTela;	

  begin
 
  end;


  procedure Somatorio(entrada:integer);
   
  var
      
     resultado: integer; {Declare a variável "a" novamente. Neste caso não deve gerar erro poiso escopo é outro}
  
  begin
   
     resultado := 0;
      
     {LimparTela; adicione este procedimento}
     while (entrada>0) do {no lugar de "entrada" use "input" e veja se gera o erro "variável não declarada" }
                         resultado := resultado + entrada;
     entrada := entrada - 1
             {troque "1" por "chave" e veja se gera o erro "tipos incompatíveis"}	
     
  end;


begin
   
   LimparTela;

   x:= y + z * (5.5 - c) / 2.567; {troque "x" por "a" e veja se gera o erro "tipos incompatíveis"}
  
   if chave then 

      if x <> z then {substitua x por chave} 
 
         z := 5.0 {troque "5.0" por "test1" e veja se gera erro "Nome do programa não pode ser usado"}
  
      else
   
      chave := not chave

end.
"""

def memory_usage():
    process = psutil.Process()
    mem = process.memory_info().rss / 1024 / 1024
    return mem

#Manda o código para o lexer
lexico = Lexer(codigo_pascal)
#Armazena os tokens
tokens = lexico.tokens
#manda tokens para o parser
sintatico = Parser(tokens)

try:
    #tenta fazer o parser e fala se tiver problema ou não
    sintatico.programa()
    print("Parser OK")
    end_time = time.time()
    tempo = end_time - start_time
    print(f"Tempo: {tempo* 1000:.3f} ms")
    print(f'Memória utilizada: {memory_usage()} MB')
    
except SyntaxError as e:
    print(f"SyntaxError: {e}")