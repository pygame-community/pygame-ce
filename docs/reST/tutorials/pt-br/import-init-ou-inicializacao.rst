.. TUTORIAL: Importação e Inicialização

.. include:: ../../common.txt

****************************************************
  Tutoriais do Pygame - Importação e Inicialização
****************************************************

Importação e Inicialização
==========================

.. rst-class:: docinfo

:Author: Pete Shinners
:Contact: pete@shinners.org


Importação
----------

Importar e inicializar o pygame é um processo muito simples. Também é
flexível o suficiente para lhe dar controle sobre o que está acontecendo. Pygame é um
conjunto de diferentes módulos em um único pacote python. Alguns dos
módulos são escritos em C, e alguns são escritos em python. Alguns módulos
também são opcionais e podem não estar sempre presentes.

Esta é apenas uma breve introdução sobre o que está acontecendo quando você importa o pygame.
Para uma explicação mais clara, consulte definitivamente os exemplos do pygame.


Importação
----------

Primeiro, devemos importar o pacote pygame. Desde a versão 1.4 do pygame,
isso foi atualizado para ser muito mais fácil. A maioria dos jogos importará todo o pygame assim. ::

  import pygame
  from pygame.locals import *

A primeira linha aqui é a única necessária. Ela importa todos os módulos pygame
disponíveis no pacote pygame. A segunda linha é opcional e coloca um conjunto limitado
de constantes e funções no namespace global do seu script.

Uma coisa importante a ter em mente é que vários módulos do pygame são opcionais.
Por exemplo, um deles é o módulo de fonte. Quando você "importa pygame", o pygame
verificará se o módulo de fonte está disponível. Se o módulo de fonte estiver disponível,
ele será importado como "pygame.font". Se o módulo não estiver disponível, "pygame.font"
será definido como None. Isso facilita verificar mais tarde se o módulo de fonte está disponível.


Inicialização
-------------

Antes de poder fazer muito com o pygame, será necessário inicializá-lo. A maneira mais comum
de fazer isso é apenas fazer uma chamada. ::

  pygame.init()

Isso tentará inicializar todos os módulos do pygame para você. Nem todos os módulos do pygame
precisam ser inicializados, mas isso inicializará automaticamente aqueles que precisam. Você pode
também inicializar facilmente cada módulo do pygame manualmente. Por exemplo, para inicializar apenas o
módulo de fonte, você chamaria apenas. ::

  pygame.font.init()

Observe que se houver um erro ao inicializar com "pygame.init()", ele falhará silenciosamente.
Ao inicializar manualmente módulos dessa forma, quaisquer erros gerarão uma exceção. Todos os
módulos que precisam ser inicializados também têm uma função "get_init()", que retornará verdadeiro
se o módulo tiver sido inicializado.

É seguro chamar a função init() para qualquer módulo mais de uma vez.


Sair
----

Módulos que são inicializados também costumam ter uma função quit() que fará a limpeza.
Não há necessidade de chamá-los explicitamente, pois o pygame encerrará limpará todos os
módulos inicializados quando o python terminar.
