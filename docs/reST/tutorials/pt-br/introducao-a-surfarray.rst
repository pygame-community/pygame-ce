.. TUTORIAL: Introdução ao módulo surfarray

.. include:: ../../common.txt

**********************************************
  Tutoriais Pygame - Introdução ao Surfarray
**********************************************

.. currentmodule:: surfarray

Introdução ao Surfarray
=======================

.. rst-class:: docinfo

:Author: Pete Shinners
:Contacto: pete@shinners.org


Introdução
----------

Este tutorial tentará introduzir os usuários tanto ao NumPy quanto ao módulo
surfarray do pygame. Para iniciantes, o código que usa surfarray pode ser bastante
intimidante. Mas na verdade, existem apenas alguns conceitos para entender e
você estará pronto para começar. Usando o módulo surfarray, torna-se possível
realizar operações no nível de pixel a partir de código Python puro. O desempenho
pode se tornar bastante próximo do nível de escrever o código em C.

Você pode querer pular para a seção *"Exemplos"* para ter uma
ideia do que é possível com este módulo, depois comece do início aqui
para evoluir.

Agora, eu não vou tentar te enganar pensando que tudo é muito fácil. Para obter
efeitos mais avançados modificando os valores dos pixels é muito complicado. Dominar
o NumPy (o pacote original de arrays do SciPy era o Numeric, o predecessor do NumPy)
requer muita aprendizagem. Neste tutorial, vou ficar com
o básico e usar muitos exemplos na tentativa de plantar sementes de sabedoria.
Depois de terminar o tutorial, você deverá ter uma compreensão básica de como o surfarray
funciona.

NumPy
-----

Se você não tiver o pacote python NumPy instalado,
você precisará fazer isso agora, seguindo o
`Guia de Instalação do NumPy <https://numpy.org/install/>`_.
Para ter certeza de que o NumPy está funcionando para você,
você deve obter algo assim no prompt interativo do Python. ::

  >>> from numpy import *                    #import numeric
  >>> a = array((1,2,3,4,5))                 #criar uma matriz
  >>> a                                      #exibir a matriz
  array([1, 2, 3, 4, 5])
  >>> a[2]                                   #indexar na matriz
  3
  >>> a*2                                    #nova matriz com valores dobrados
  array([ 2,  4,  6,  8, 10])

Como você pode ver, o módulo NumPy nos dá um novo tipo de dado, o *array*.
Este objeto contém uma matriz de tamanho fixo, e todos os valores dentro são do mesmo
tipo. As matrizes também podem ser multidimensionais, que é como vamos usá-las
com imagens. Há um pouco mais do que isso, mas é o suficiente para começarmos.

Se você olhar o último comando acima, verá que as operações matemáticas
em matrizes NumPy se aplicam a todos os valores na matriz. Isso é chamado de "operação
element-wise". Essas matrizes também podem ser fatiadas como listas normais. A sintaxe de fatiamento
é a mesma usada em objetos python padrão.
*(então estude se precisar :] )*.
Aqui estão mais alguns exemplos de trabalho com matrizes. ::

  >>> len(a)                                 #obter o tamanho da matriz
  5
  >>> a[2:]                                  #elementos a partir do 2
  array([3, 4, 5])
  >>> a[:-2]                                 #todos exceto os últimos 2
  array([1, 2, 3])
  >>> a[2:] + a[:-2]                         #adicionar o primeiro e o último
  array([4, 6, 8])
  >>> array((1,2,3)) + array((3,4))          #adicionar matrizes de tamanhos diferentes
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  ValueError: operands could not be broadcast together with shapes (3,) (2,)

Obtemos um erro no último comando, porque tentamos adicionar duas matrizes
que têm tamanhos diferentes. Para que duas matrizes operem entre si,
incluindo comparações e atribuição, elas devem ter as mesmas dimensões. É
muito importante saber que as novas matrizes criadas ao fatiar a original
referenciam todos os mesmos valores. Portanto, alterar os valores em uma fatia também altera os
valores originais. É importante entender como isso é feito. ::

  >>> a                                      #mostrar nossa matriz inicial
  array([1, 2, 3, 4, 5])
  >>> aa = a[1:3]                            #fatiar os 2 elementos do meio
  >>> aa                                     #mostrar a fatia
  array([2, 3])
  >>> aa[1] = 13                             #mudar o valor na fatia
  >>> a                                      #mostrar a mudança no original
  array([ 1, 2, 13,  4,  5])
  >>> aaa = array(a)                         #fazer uma cópia da matriz
  >>> aaa                                    #mostrar cópia
  array([ 1, 2, 13,  4,  5])
  >>> aaa[1:4] = 0                           #definir os valores do meio como 0
  >>> aaa                                    #mostrar cópia
  array([1, 0, 0, 0, 5])
  >>> a                                      #mostrar original novamente
  array([ 1, 2, 13,  4,  5])

Agora vamos olhar para matrizes pequenas com duas
dimensões. Não se preocupe muito, começar é o mesmo que ter um
tupla bidimensional *(uma tupla dentro de uma tupla)*. Vamos começar com
matrizes bidimensionais. ::

  >>> row1 = (1,2,3)                         #criar uma tupla de valores
  >>> row2 = (3,4,5)                         #outra tupla
  >>> (row1,row2)                            #mostrar como uma tupla 2D
  ((1, 2, 3), (3, 4, 5))
  >>> b = array((row1, row2))                #criar uma matriz 2D
  >>> b                                      #mostrar a matriz
  array([[1, 2, 3],
         [3, 4, 5]])
  >>> array(((1,2),(3,4),(5,6)))             #mostrar uma nova matriz 2D
  array([[1, 2],
         [3, 4],
         [5, 6]])

Agora com esta matriz bidimensional *(a partir de agora chamada "2D")*,
podemos indexar valores específicos
e fazer fatias em ambas as dimensões. Simplesmente usando uma vírgula para separar os índices
nos permite procurar/fatiar em várias dimensões. Apenas usando "``:``" como um
índice *(ou não fornecendo índices suficientes)* nos dá todos os valores em
essa dimensão. Vamos ver como isso funciona. ::

  >>> b                                      #mostrar nossa matriz de cima
  array([[1, 2, 3],
         [3, 4, 5]])
  >>> b[0,1]                                 #indexar um único valor
  2
  >>> b[1,:]                                 #fatiar a segunda linha
  array([3, 4, 5])
  >>> b[1]                                   #fatiar a segunda linha (mesmo que acima)
  array([3, 4, 5])
  >>> b[:,2]                                 #fatiar a última coluna
  array([3, 5])
  >>> b[:,:2]                                #fatiar em uma matriz 2x2
  array([[1, 2],
         [3, 4]])

Ok, fique comigo aqui, isso é mais difícil do que parece. Ao usar o NumPy
há mais uma característica para fatiar. Fatiar matrizes também permite que você especifique
um *incremento de fatia*. A sintaxe para uma fatia com incremento é
``start_index : end_index : increment``. ::

  >>> c = arange(10)                         #como range, mas faz uma matriz
  >>> c                                      #mostrar a matriz
  array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
  >>> c[1:6:2]                               #fatiar valores ímpares de 1 a 6
  array([1, 3, 5])
  >>> c[4::4]                                #fatiar a cada 4º valor a partir de 4
  array([4, 8])
  >>> c[8:1:-1]                              #fatiar de 1 a 8, invertido
  array([8, 7, 6, 5, 4, 3, 2])

Bem, é isso. Há informações suficientes para começar a usar
NumPy com o módulo surfarray. Certamente há muito mais para aprender sobre o NumPy, mas
isso é apenas uma introdução. Além disso, queremos ir para as coisas divertidas,
certo?


Importar Surfarray
------------------

Para usar o módulo surfarray, precisamos importá-lo. Como tanto surfarray
quanto NumPy são componentes opcionais para o pygame, é bom garantir que eles
sejam importados corretamente antes de usá-los. Nestes exemplos, vou importar
o NumPy em uma variável chamada *N*. Isso permitirá que você saiba quais funções
estou usando são do pacote NumPy.
*(e é muito mais curto do que digitar NumPy antes de cada função)* ::

  try:
      import numpy as N
      import pygame.surfarray as surfarray
  except ImportError:
      raise ImportError, "NumPy e Surfarray são necessários."


Introdução ao Surfarray
-----------------------


Existem dois tipos principais de funções em surfarray. Um conjunto de funções para
criar uma matriz que é uma cópia dos dados de pixel de uma superfície. As outras funções
criam uma cópia referenciada dos dados de pixel da matriz, para que as alterações na matriz
afetem diretamente a superfície original. Existem outras funções que permitem
acessar quaisquer valores de alfa por pixel como matrizes, junto com algumas outras funções úteis.
Vamos ver essas outras funções mais tarde.

Ao trabalhar com essas matrizes de superfície, existem duas maneiras de representar os
valores de pixel. Primeiro, eles podem ser representados como inteiros mapeados. Este tipo de
matriz é uma matriz 2D simples com um único inteiro representando o valor de cor mapeada da superfície.
Este tipo de matriz é bom para mover partes de uma imagem
ao redor. O outro tipo de matriz usa três valores RGB para representar cada pixel
cor. Este tipo de matriz torna extremamente simples fazer tipos de efeitos que
mudam a cor de cada pixel. Este tipo de matriz também é um pouco mais complicado de
lidar, já que é essencialmente uma matriz numérica 3D. Ainda assim, uma vez que você coloca sua
mente no modo certo, não é muito mais difícil do que usar as matrizes normais 2D.

O módulo NumPy usa os tipos de número naturais da máquina para representar os dados
valores, então uma matriz NumPy pode consistir em inteiros de 8 bits, 16 bits e 32 bits.
*(as matrizes também podem usar outros tipos como floats e doubles, mas para nossa imagem
manipulação, principalmente precisamos nos preocupar com os tipos inteiros)*.
Devido a essa limitação de tamanhos de inteiros, você deve ter um pouco mais de cuidado
que o tipo de matrizes que referenciam dados de pixels possa ser adequadamente mapeado para um
tipo adequado de dados. As funções que criam essas matrizes a partir de superfícies são:

.. function:: pixels2d(surface)
   :noindex:

   Cria uma matriz 2D *(valores de pixel inteiros)* que faz referência aos dados originais da superfície.
   Isso funcionará para todos os formatos de superfície, exceto 24 bits.

.. function:: array2d(surface)
   :noindex:

   Cria uma matriz 2D *(valores de pixel inteiros)* que é copiada de qualquer tipo de superfície.

.. function:: pixels3d(surface)
   :noindex:

   Cria uma matriz 3D *(valores de pixel RGB)* que faz referência aos dados originais da superfície.
   Isso só funcionará em superfícies de 24 bits e 32 bits que têm formatação RGB ou BGR.

.. function:: array3d(surface)
   :noindex:

   Cria uma matriz 3D *(valores de pixel RGB)* que é copiada de qualquer tipo de superfície.

Aqui está um pequeno gráfico que pode ilustrar melhor quais tipos de funções
devem ser usadas em quais superfícies. Como você pode ver, ambas as funções arrayXD
funcionarão com qualquer tipo de superfície.

.. csv-table::
   :class: matrix
   :header: , "32 bits", "24 bits", "16 bits", "8 bits (c-map)"
   :widths: 15, 15, 15, 15, 15
   :stub-columns: 1

   "pixels2d", "sim",      , "sim", "sim"
   "array2d", "sim", "sim", "sim", "sim"
   "pixels3d", "sim", "sim",      ,
   "array3d", "sim", "sim", "sim", "sim"

Exemplos
--------

Com estas informações, estamos preparados para começar a experimentar com arrays de superfície. A seguir, há demonstrações breves que criam um array NumPy e os exibem no Pygame. Esses testes diferentes são encontrados no exemplo *arraydemo.py*. Existe uma função simples chamada *surfdemo_show* que exibe um array na tela.

.. container:: examples

   .. container:: example

      .. image:: ../assets/surfarray_allblack.png
         :alt: allblack

      ::

        allblack = N.zeros((128, 128))
        surfdemo_show(allblack, 'allblack')

      Nosso primeiro exemplo cria um array totalmente preto. Sempre que você precisar
      criar um novo array numérico de um tamanho específico, é melhor usar a função
      ``zeros``. Aqui, criamos um array 2D de todos os zeros e o exibimos.

      .. container:: break

         ..

   .. container:: example

      .. image:: ../assets/surfarray_striped.png
         :alt: striped

      ::

        striped = N.zeros((128, 128, 3))
        striped[:] = (255, 0, 0)
        striped[:,::3] = (0, 255, 255)
        surfdemo_show(striped, 'striped')

      Aqui lidamos com um array 3D. Começamos criando uma imagem totalmente vermelha.
      Em seguida, fatiamos a cada terceira linha e atribuímos a ela uma cor azul/verde. Como você
      pode ver, podemos tratar os arrays 3D quase exatamente da mesma forma que os arrays 2D, apenas
      certifique-se de atribuir a eles 3 valores em vez de um único valor inteiro mapeado.

      .. container:: break

         ..

   .. container:: example

      .. image:: ../assets/surfarray_rgbarray.png
         :alt: rgbarray

      ::

        imgsurface = pygame.image.load('surfarray.png')
        rgbarray = surfarray.array3d(imgsurface)
        surfdemo_show(rgbarray, 'rgbarray')

      Aqui, carregamos uma imagem com o módulo de imagem e, em seguida, a convertemos em um array 3D
      de elementos de cor RGB inteiros. Uma cópia RGB de uma superfície sempre
      tem as cores dispostas como a[r,c,0] para o componente vermelho,
      a[r,c,1] para o componente verde e a[r,c,2] para azul. Isso pode ser então
      usado sem se preocupar com a configuração dos pixels da superfície real,
      ao contrário de um array 2D que é uma cópia dos pixels da superfície bruta
      (raw) através do método :meth:`mapped <pygame.Surface.map_rgb>`. Vamos usar esta imagem no restante dos exemplos.

      .. container:: break

         ..

   .. container:: example

      .. image:: ../assets/surfarray_flipped.png
         :alt: flipped

      ::

        flipped = rgbarray[:,::-1]
        surfdemo_show(flipped, 'flipped')

      Aqui, invertemos a imagem verticalmente. Tudo o que precisamos fazer é pegar o array original
      da imagem e fatiá-lo usando um incremento negativo.

      .. container:: break

         ..

   .. container:: example

      .. image:: ../assets/surfarray_scaledown.png
         :alt: scaledown

      ::

        scaledown = rgbarray[::2,::2]
        surfdemo_show(scaledown, 'scaledown')

      Com base no exemplo anterior, reduzir o tamanho de uma imagem é bastante lógico. Apenas
      fatiamos todos os pixels usando um incremento de 2 vertical e horizontalmente.

      .. container:: break

         ..


   .. container:: example

      .. image:: ../assets/surfarray_scaleup.png
         :alt: scaleup

      ::

        shape = rgbarray.shape
        scaleup = N.zeros((shape[0]*2, shape[1]*2, shape[2]))
        scaleup[::2,::2,:] = rgbarray
        scaleup[1::2,::2,:] = rgbarray
        scaleup[:,1::2] = scaleup[:,::2]
        surfdemo_show(scaleup, 'scaleup')

      Aumentar o tamanho da imagem é um pouco mais trabalhoso, mas é semelhante ao redimensionamento anterior.
      Fazemos tudo com fatias. Primeiro, criamos um array que é
      o dobro do tamanho do original. Primeiro, copiamos o array original em cada
      outro pixel do novo array. Então fazemos isso novamente para cada outro pixel, nas colunas ímpares. Neste ponto, temos a imagem dimensionada corretamente atravessando,
      mas toda outra linha é preta, então simplesmente precisamos copiar cada linha para a linha de baixo.
      Então temos uma imagem duplicada em tamanho.

      .. container:: break

         ..


   .. container:: example

      .. image:: ../assets/surfarray_redimg.png
         :alt: redimg

      ::

        redimg = N.array(rgbarray)
        redimg[:,:,1:] = 0
        surfdemo_show(redimg, 'redimg')

      Agora estamos usando arrays 3D para alterar as cores. Aqui nós
      definimos todos os valores em verde e azul como zero.
      Isso nos deixa apenas com o canal vermelho.

      .. container:: break

         ..


   .. container:: example

      .. image:: ../assets/surfarray_soften.png
         :alt: soften

      ::

        factor = N.array((8,), N.int32)
        soften = N.array(rgbarray, N.int32)
        soften[1:,:]  += rgbarray[:-1,:] * factor
        soften[:-1,:] += rgbarray[1:,:] * factor
        soften[:,1:]  += rgbarray[:,:-1] * factor
        soften[:,:-1] += rgbarray[:,1:] * factor
        soften //= 33
        surfdemo_show(soften, 'soften')

      Aqui realizamos um filtro de convolução 3x3 que suavizará nossa imagem.
      Parece que há muitas etapas aqui, mas o que estamos fazendo é deslocar
      a imagem 1 pixel em cada direção e somá-las todas (com alguma
      multiplicação para ponderação). Em seguida, fazemos a média de todos os valores. Não é um Gaussiano,
      mas é rápido. Um ponto com arrays NumPy, a precisão das operações aritméticas
      é determinada pelo array com o maior tipo de dados.
      Portanto, se o fator não foi declarado como um array de 1 elemento do tipo numpy.int32,
      as multiplicações seriam realizadas usando numpy.int8, o tipo de inteiro de 8 bits
      de cada elemento rgbarray. Isso causará truncamento de valor. O array soften
      também deve ser declarado como tendo um tamanho de inteiro maior que rgbarray para
      evitar truncamento.

      .. container:: break

         ..


   .. container:: example

      .. image:: ../assets/surfarray_xfade.png
         :alt: xfade

      ::

        src = N.array(rgbarray)
        dest = N.zeros(rgbarray.shape)
        dest[:] = 20, 50, 100
        diff = (dest - src) * 0.50
        xfade = src + diff.astype(N.uint)
        surfdemo_show(xfade, 'xfade')

      Por fim, estamos realizando uma mistura cruzada entre a imagem original e uma imagem azul sólida.
      Não é emocionante, mas a imagem de destino pode ser qualquer coisa, e alterar o multiplicador 0.50
      permitirá escolher qualquer etapa em uma mistura cruzada linear entre duas imagens.

      .. container:: break

         ..

Neste ponto, espero que você esteja começando a ver como surfarray pode ser usado para
realizar efeitos especiais e transformações que são possíveis apenas no nível de pixel.
No mínimo, você pode usar o surfarray para fazer muitas operações do tipo Surface.set_at()
Surface.get_at() muito rapidamente. Mas não pense que você terminou
ainda, há muito mais a aprender.


Bloqueio de Superfície
----------------------

Como o restante do pygame, surfarray bloqueará qualquer superfície que precise
automaticamente ao acessar dados de pixel. No entanto, há mais uma coisa a ter em mente.
Ao criar os arrays de *pixel*, a superfície original será
bloqueada durante a vida útil desse array de pixel. Isso é importante lembrar.
Certifique-se de *"excluir"* o array de pixel ou deixá-lo sair de escopo
*(ou seja, quando a função retornar, etc.)*.

Esteja ciente também de que você realmente não deseja fazer muita coisa *(se houver alguma)*
acesso direto de pixels em superfícies de hardware *(HWSURFACE)*. Isso ocorre porque
os dados reais da superfície residem na placa gráfica e transferir pixels
alterações pela barramento PCI/AGP não é rápido.


Transparência
-------------

O módulo surfarray possui vários métodos para acessar os valores alfa/colorkey
de uma superfície. Nenhuma das funções alfa é afetada pela transparência geral de um
Superfície, apenas os valores alfa do pixel. Aqui está a lista dessas funções.

.. function:: pixels_alpha(surface)
   :noindex:

   Cria um array 2D *(valores de pixel inteiros)* que referencia os dados alfa originais
   da superfície. Isso só funcionará em imagens de 32 bits com um componente alfa de 8 bits.

.. function:: array_alpha(surface)
   :noindex:

   Cria um array 2D *(valores de pixel inteiros)* que é copiado de qualquer
   tipo de superfície. Se a superfície não tiver valores alfa,
   o array terá valores totalmente opacos *(255)*.

.. function:: array_colorkey(surface)
   :noindex:

   Cria um array 2D *(valores de pixel inteiros)* que é definido como transparente
   *(0)* onde a cor do pixel corresponde à cor de chave da Superfície.


Outras Funções de Surfarray
---------------------------

Existem apenas algumas outras funções disponíveis em surfarray. Você pode obter uma lista melhor
com mais documentação na
:mod:`página de referência do surfarray <pygame.surfarray>`.
No entanto, há uma função muito útil.

.. function:: surfarray.blit_array(surface, array)
   :noindex:
   
   Isso transferirá qualquer tipo de array de superfície 2D ou 3D para uma Superfície
   das mesmas dimensões. Este blit de surfarray geralmente será mais rápido do que atribuir um array a um
   array de pixel referenciado. Ainda assim, não deve ser tão rápido quanto o blit normal de Surface,
   já que estes são muito otimizados.


NumPy Mais Avançado
-------------------

Há mais algumas coisas que você deve saber sobre os arrays NumPy. Ao lidar
com arrays muito grandes, como os de tamanho 640x480, há algumas coisas adicionais
que você deve ter cuidado. Principalmente, ao usar operadores como + e
* nos arrays, eles os tornam fáceis de usar, mas também são muito caros em grandes arrays.
Esses operadores precisam criar cópias temporárias do array, que são então
geralmente copiadas para outro array. Isso pode se tornar muito demorado. Felizmente,
todos os operadores NumPy vêm com funções especiais que podem realizar a
operação *"in-place"*. Por exemplo, você gostaria de substituir
``screen[:] = screen + brightmap`` pelo muito mais rápido
``add(screen, brightmap, screen)``.
De qualquer forma, você vai querer ler sobre o UFunc do NumPy
documentação para saber mais sobre isso.
Isso é importante ao lidar com os arrays.

Outra coisa a se estar ciente ao trabalhar com arrays NumPy é o tipo de dado
do array. Alguns dos arrays (especialmente o tipo de pixel mapeado) frequentemente retornam
arrays com um valor de 8 bits sem sinal. Esses arrays facilmente transbordarão se você não estiver
cuidadoso. NumPy usará a mesma coerção que você encontra em programas em C, então
misturar uma operação com números de 8 bits e números de 32 bits dará um resultado como
números de 32 bits. Você pode converter o tipo de dado de um array, mas definitivamente esteja
ciente dos tipos de arrays que você tem, se o NumPy entrar em uma situação onde a
precisão seria arruinada, ele lançará uma exceção.

Por fim, esteja ciente de que ao atribuir valores aos arrays 3D, eles devem ser
entre 0 e 255, ou você obterá uma truncagem indefinida.


Graduação
---------

Bem, aí está. Meu breve guia sobre NumPy e surfarray.
Espero que agora você veja o que é possível, e mesmo que você nunca use para
você mesmo, você não precisa ter medo quando vir um código que usa isso. Olhe para
o exemplo de vgrade para mais ação de arrays numéricos. Também existem alguns demos de *"chamas"*
flutuando por aí que usam surfarray para criar um efeito de fogo em tempo real.

O melhor de tudo, experimente algumas coisas por conta própria. Vá devagar no início e construa,
já vi algumas coisas ótimas com surfarray, como gradientes radiais e
mais. Boa sorte.
