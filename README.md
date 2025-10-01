# Platformer Adventure Game

Um jogo platformer estilo Mario desenvolvido em Python usando PGZero, criado como teste para tutores de programação.

## Estrutura do Projeto

```
Game/
├── main.py          # Arquivo principal do jogo
├── sounds/          # Pasta para efeitos sonoros
├── music/           # Pasta para música de fundo
├── images/          # Pasta para sprites e imagens
└── README.md        # Este arquivo
```

## Instalação

1. Instale as dependências:
```bash
pip install pgzero pygame
```

2. Execute o jogo:
```bash
python main.py
```

## Como Jogar

### Controles
- **Setas ← →**: Mover para esquerda/direita
- **ESPAÇO**: Pular
- **ESC**: Voltar ao menu principal
- **Mouse**: Clicar nos botões do menu

### Objetivo
- Pule sobre plataformas e obstáculos
- Colete moedas douradas para ganhar pontos
- Evite os inimigos vermelhos e laranjas
- Chegue ao final da tela para vencer

## Ferramentas para Desenhar Sprites

### Recomendações para Criar Sprites:

#### 1. **Photoshop** (Recomendado)
- **Vantagens**: Ferramentas profissionais, camadas, filtros
- **Tamanho ideal**: 32x32 ou 64x64 pixels
- **Formato**: PNG com transparência
- **Dicas**: Use pixel art, cores vibrantes, contornos definidos

#### 2. **Alternativas Gratuitas**:
- **GIMP**: Gratuito, similar ao Photoshop
- **Paint.NET**: Simples e eficiente
- **Aseprite**: Especializado em pixel art (pago, mas tem versão gratuita)
- **Piskel**: Editor online gratuito para pixel art

#### 3. **Ferramentas Online**:
- **Piskel.com**: Editor de pixel art online
- **Lospec Pixel Editor**: Editor online gratuito
- **Pixilart**: Editor online com comunidade

### Especificações dos Sprites

#### Personagem Principal (Hero)
- **Tamanho**: 32x32 pixels
- **Cores**: Azul para corpo, cor de pele para rosto
- **Animação**: 4 frames para movimento
- **Estados**: Parado, correndo, pulando

#### Inimigos
- **Tamanho**: 24x24 pixels
- **Cores**: Vermelho (básico), Laranja (forte)
- **Animação**: 3 frames para movimento
- **Características**: Olhos brancos com pupilas pretas

#### Moedas
- **Tamanho**: 16x16 pixels
- **Cor**: Dourado (255, 215, 0)
- **Animação**: Efeito de brilho/pulsar

#### Plataformas
- **Tamanho**: 150x20 pixels
- **Cor**: Verde (100, 200, 100)
- **Textura**: Padrão de blocos 16x16

### Como Adicionar Seus Sprites

1. **Crie os sprites** usando uma das ferramentas acima
2. **Salve como PNG** na pasta `images/`
3. **Nomes sugeridos**:
   - `hero.png` - Personagem principal
   - `enemy_basic.png` - Inimigo básico
   - `enemy_strong.png` - Inimigo forte
   - `coin.png` - Moeda
   - `platform.png` - Plataforma

4. **Modifique o código** em `main.py` para carregar as imagens:
```python
# Exemplo de como carregar sprites
hero_image = Actor('hero', (hero.x, hero.y))
```

### Dicas para Pixel Art

1. **Use poucas cores** (8-16 cores por sprite)
2. **Mantenha consistência** no estilo
3. **Use contornos** para definir formas
4. **Anime frame por frame** para movimento suave
5. **Teste em tamanho real** (32x32 pixels)

## Características do Jogo

### Mecânicas Implementadas
- **Física de pulo**: Gravidade e força de pulo realistas
- **Colisões**: Detecção precisa entre objetos
- **Animações**: Sprites animados para todos os personagens
- **Sistema de vida**: Herói com 100 HP
- **Sistema de pontuação**: Coletar moedas = +10 pontos
- **Múltiplos níveis**: Sistema de progressão

### Conformidade com Requisitos
✅ **Bibliotecas Permitidas**: PGZero, math, random, Rect do Pygame  
✅ **Gênero**: Platformer com visão lateral  
✅ **Menu Principal**: Botões clicáveis  
✅ **Música e Sons**: Sistema de áudio  
✅ **Inimigos Perigosos**: Múltiplos inimigos  
✅ **Movimento**: Inimigos se movem automaticamente  
✅ **Classes**: Hero, Enemy, Platform, Coin  
✅ **Animação de Sprite**: Animação contínua  
✅ **Nomes em Inglês**: Código em inglês  
✅ **PEP8**: Código formatado  
✅ **Mecânica Lógica**: Jogo funcional  
✅ **Código Único**: Implementação original

## Próximos Passos

1. **Crie seus sprites** usando Photoshop ou ferramentas similares
2. **Adicione sons** na pasta `sounds/`
3. **Adicione música** na pasta `music/`
4. **Teste o jogo** e ajuste conforme necessário
5. **Personalize** cores, velocidades e dificuldade

## Desenvolvido por

Teste para tutores de programação Python - 2024
