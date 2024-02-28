let moviesData = [];
let commentsData = [];
let palavrasOfensivas;
let currentMovieIndex = 0;
const apiUrl = 'http://localhost:5000/api';

async function fetchMoviesData() {
    try {
        const moviesResponse = await fetch(`${apiUrl}/movies`);
        if (!moviesResponse.ok) {
            throw new Error(`Erro ao buscar dados dos filmes`);
        }

        const moviesFetchData = await moviesResponse.json();
        moviesData = moviesFetchData.movies;

        const commentsResponse = await fetch(`${apiUrl}/comments/type/movies`);
        const commentsFetchData = await commentsResponse.json();
        commentsData = commentsFetchData.comments;
        
    } catch (moviesError) {
        // Lidar com erros aqui
        console.error(error);
        throw error; // Rejeitar a promessa para que o bloco catch posterior seja acionado
    }
}

// Inicialmente, obtenha todos os dados dos filmes
fetchMoviesData().then(() => {
    // Crie os cartões do carrossel
    if (moviesData) {
        const movieCarousel = document.getElementById('movie-carousel');
        moviesData.forEach((movie, index) => {
            const movieCard = document.createElement('div');
            movieCard.className = 'movie-card';
            movieCard.innerHTML = `<img src="${movie.image_url}" alt="${movie.title}">`;
            movieCard.addEventListener('click', () => showMovie(index));
            movieCarousel.appendChild(movieCard);
        });

        showMovie(0);
    }
    else {
        showNoMovies();
    }
}).catch((error) => {
    showNoMovies();
});

function showNoMovies() {
    const container = document.getElementById('container');
    container.innerHTML = '';
    const messageElement = document.createElement('h1');
    messageElement.textContent = 'Não há filmes disponíveis no momento';
    container.appendChild(messageElement);
}

function showMovie(index) {
    currentMovieIndex = index;
    const screenWidth = window.innerWidth;
    const movieWidth = 300;  // Substitua isso pela largura real da imagem do filme em pixels
    const spacing = 10;  // Ajuste o espaçamento conforme necessário

    // Calcula o offset para centralizar a imagem
    const offset = -(index * (movieWidth + spacing)) + (screenWidth - movieWidth) / 2;

    document.getElementById('movie-carousel').style.transform = `translateX(${offset}px)`;
    const cards = document.getElementById('movie-carousel').getElementsByClassName('movie-card');
    for (let index = 0; index < cards.length; index++) {
        cards[index].style.transform = 'scale(1)';
    }
    cards[index].style.transform = 'scale(1.1)';

    // Obtenha os dados do filme do cache
    const movieData = moviesData[index];
    const movieComments = commentsData.filter((commentData) => {return movieData.id === commentData.type_id;});

    if (movieData) {
        document.getElementById('movie-title').innerText = movieData.title;
        document.getElementById('movie-sinopse').innerText = movieData.sinopse;
        document.getElementById('movie-date').innerText = `Date: ${movieData.date}`;
        document.getElementById('movie-duration').innerText = `Duration: ${movieData.duration}`;
        document.getElementById('movie-classification').innerText = `Classification: ${movieData.classification}`;

        const commentsList = document.getElementById('comments-list');
        commentsList.innerHTML = '';
        movieComments.forEach(comment => {
            const li = document.createElement('li');
            li.textContent = comment.text;
            commentsList.appendChild(li);
        });
    }
}

// Funções para controlar a navegação
function nextMovie() {
    showMovie((currentMovieIndex < moviesData.length - 1) ? currentMovieIndex + 1 : 0);
}

function prevMovie() {
    showMovie((currentMovieIndex > 0) ? currentMovieIndex - 1 : moviesData.length - 1);
}

async function addComment() {
    const commentInput = document.getElementById('comment-input');
    const commentText = commentInput.value;

    if (commentText.trim() !== '' && verificaComentario(commentText)) {
        const commentsList = document.getElementById('comments-list');
        const newComment = document.createElement('li');
        newComment.textContent = commentText;
        commentsList.appendChild(newComment);
        commentInput.value = '';

        try {
            // Enviar o comentário para a API
            const response = await fetch(`${apiUrl}/comments`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: 1,
                    type_id: moviesData[currentMovieIndex]['id'],
                    type: 'movies',
                    text: commentText,
                    date: new Date().toISOString().slice(0, 19).replace("T", " ")
                }),
            });

            if (response.ok) {
                // Comentário enviado com sucesso
                commentsData.push({
                    type: 'movies',
                    type_id: moviesData[currentMovieIndex]['id'],
                    text: commentText,
                });

            } else {
                // Lidar com erro ao enviar comentário
                console.error('Erro ao enviar comentário:', response.status, response.statusText);
                newComment.textContent = 'Comentário não pôde ser adicionado';
            }
        } catch (error) {
            // Lidar com exceções
            console.error('Erro ao enviar comentário:', error);
            newComment.textContent = 'Comentário não pôde ser adicionado';
        }  
    }
}

async function getPalavrasOfensivas() {
    try {
        palavras = `Vadia
Safada
Vagabunda
Pobre
Desgraçada
Prostituta
Rapariga
Esquisita
Esquizofrênica
Chata
Cadeirante
Feia
Aleijada
Aloprada
Atropelada
Burra
Idiota
Cachorra
Cadela
Presidiária
Fedida
Otaka
Degenerada
Gorda
Louca
Monoteta
Arrombada
Bunda
Descabelada
Vaca
Imbecil
Véia
Meretriz
Mal comida
Arrebentada
Lixo
Chorume
Puta
Corna
Peluda
Merda
Bosta
Porra
Ignorante
burro
idiota
imbecil
retardado
analfabeto
boçal
bronco
estúpido
iletrado
ignaro
onagro
inculto
obsoleto
retrógado
beócio
rude
desaforado
descortês
estólido
inepto
lambão
obtuso
palerma
sandeu
toupeira
incapaz
insensato
imperito
impróprio
inapto
inábil
abagualado
bárbaro
labrusco
sáfaro
insciente
inepto
insipiente
imprudente
leigo
alheio
estranho
profano
estulto
fátuo
mentecapto
pateta
toleirão
írrito
vão
oco
chocho
frívolo
fútil
definhado
enfezado
frustrado
abeutalhado
agreste
chambão
cavalar
desabrido
escabroso
fragoso
incivil
inclemente
indelicado
inóspito
reboto
ríspido
rombudo
tacanho
tosco
covarde
poltrão
safado
baldo
infundado
mentido
metido
nugativo
supervacâneo
bordegão
asinário
bordalengo
calino
indouto
sinistro
arrogante
desinformado
alvar
atoleimado
estúpido
boçal
bronco
Disparatado
rude
azêmola
lanzudo
brutal
asselvajado
bestial
protervo
selvagem
truculento
violento
chulo
irracional
javardo
malcriado
desaforado
atrevido
insolente
descortês
inconveniente
indelicado
intratável
confragoso
cruel
despiedado
penoso
tirano
estólido
estouvado
néscio
abarroado
abrutalhado
achamboado achavascado
bárbaro
chaboqueiro
crasso
desabrido
labrego
demiurgo
maleducado
rugoso
rústico
soez
tarimbeiro
abestalhado
aluado
babão
bobalhão
bobo
bocó
demente
descerebrado
desequilibrado
desmiolado
lerdaço
paspalhão
pastranho
sendeiro
toupeira
vão
bestialógico
insociável
mal humorado
ranzinza
soberbo
panema
embotado
escabroso
inclemente
carniceiro
safado
entupido
obducto
boto
agro
balordo
Abafa a palhinha
abécula
abelhudo
abichanado
agarrado
agiota
agressivo
alarve
alcouceira
alcoviteira
aldrabão
aleivoso
amalucado
amaneirado
amaricado
amigo da onça
amigo da onça
analfabruto
apanhado do clima
aparvalhada
apóstata
arrelampado
artolas
arruaceiro
aselha
asno
asqueroso
assassino
atarantada
atrasado mental
atraso de vida
avarento
avaro
ave rara
aventesma
azeiteiro
Bbacoco
bácoro
badalhoca
badameco
baixote
bajulador
baldas
baleia
balhelhas
balofo
bandalho
bandido
barata tonta
bárbaro
bardajona
bardamerdas
bargante
barrigudo
basbaque
basculho
básico
bastardo
batoque
batoteiro
beata
bebedanas
bêbedo
bebedolas
beberrão
besta
besta quadrada
betinho
bexigoso
bichona
bicho do mato
biltre
bimbo
bisbilhoteira
boateiro
bobo
boca de xarroco
boçal
bófia
borracho
borra botas
brochista
bronco
brutamontes
bruxa
bufo
burgesso
burlão
burro
Cabeça de abóbora
cabeça de alho chôcho
cabeça de vento
cabeça no ar
cabeça oca
cabeçudo
cabotino
cabrão
cábula
caceteiro
cacique
caco
cadela
caga leite
caga tacos
cagão
caguinchas
caixa de óculos
calaceiro
calão
calhandreira
calhordas
calinas
caloteiro
camafeu
campónio
canalha
canastrão
candongueiro
caquética
cara de cu à paisana
carapau de corrida
carniceiro
carraça
carrancudo
carroceiro
casca grossa
casmurro
cavalgadura
cavalona
cegueta
celerado
cepo
chalado
chanfrado
charlatão
chatarrão
chato
chauvinista
chibo
chico esperto
chifrudo
choné
choninhas
choramingas
chulo
chunga
chupado das carochas
chupista
cigano
cínico
cobarde
covarde
cobardolas
coirão
comuna
cona de sabão
convencido
copinho de leite
corcunda
corno
cornudo
corrupto
coscuvilheira
coxo
crápula
cretino
cromo
cromaço
criminoso
cunanas
cusca
Ddebochado
delambida
delinquente
demagogo
demente
demónio
depravado
desajeitado
desastrada
desaustinado
desavergonhada
desbocado
desbragado
descabelada
desdentado
desengonçado
desgraçado
deshumano
deslavado
desleal
desmancha prazeres
desmazelada
desmiolado
desengonçado
desenxabida
desonesto
despistado
déspota
destrambelhado
destravada
destroço
desvairado
devasso
diabo
ditador
doidivanas
doido varrido
dondoca
doutor da mula russa
drogado
Eegoísta
embirrento
embusteiro
empata fodas
empecilho
emplastro
enconado
energúmeno
enfadonho
enfezado
engraxador
enjoado da trampa
enrabador
escanifobética
escanzelada
escarumba
escrofuloso
escroque
escumalha
esgalgado
esganiçada
esgroviada
esguedelhado
espalha brasas
espalhafatoso
espantalho
esparvoado
esqueleto vaidoso
esquerdista
estafermo
estapafúrdio
estouvada
estroina
estropício
estulto
estúpido
estupor
Ffaccioso
facínora
fala barato
falhado
falsário
falso
fanático
fanchono
fanfarrão
fantoche
fariseu
farrapo
farropilha
farsante
farsolas
fatela
fedelho
feia comó demo
fersureira
figurão
filho da mãe
filho da puta
fingido
fiteiro
flausina
foção
fodido
fodilhona
foleiro
forreta
fraco de espírito
fraca figura
franganote
frangueiro
frasco
frígida
frícolo
frouxo
fufa
fuinha
fura greves
fútil
Ggabarola
gabiru
galdéria
galinha choca
ganancioso
gandim
gandulo
garganeira
gato pingado
gatuno
gazeteiro
glutão
gordalhufo
gordo
gosma
gralha
grosseiro
grotesco
grunho
guedelhudo
Hherege
hipócrita
histérica
Iidiota
ignorante
imaturo
imbecil
impertinente
impostor
incapaz
incompetente
inconveniente
indecente
indigente
indolente
inepto
infame
infeliz
infiel
imprudente
intriguista
intrujona
invejoso
insensivel
insignificante
insípido
insolente
intolerante
intriguista
inútil
irritante
Jjavardo
judeu
Llabrego
labroste
lacaio
ladrão
lambão
lambareiro
lambe botas
lambéconas
lambisgóia
lamechas
lapa
larápio
larilas
lavajão
lerdo
lesma
leva e traz
libertino
limitado
língua de trapos
língua viperina
linguareira
lingrinhas
lontra
lorpa
louco
lunático
Mmá rês
madraço
mafioso
maganão
magricela
malcriado
mal enjorcado
mal fodida
malacueco
malandreco
malandrim
malandro
malfeitor
maltrapilho
maluco
malvado
mamalhuda
mandrião
maneta
mangas de alpaca
manhoso
maníaco
manipulador
maniqueista
manteigueiro
maquiavélico
marado dos cornos
marafado
marafona
marginal
maria vai com as outras
maricas
mariconço
mariola
mariquinhas pé de salsa
marmanjo
marrão
marreco
masoquista
mastronço
matarroano
matrafona
matrona
mau
medíocre
medricas
medroso
megera
meia leca
meia tijela
melga
meliante
menino da mamã
mentecapto
mentiroso
merdas
merdoso
mesquinho
metediço
mijão
mimado
mineteiro
miserável
mixordeiro
moina
molengão
mongas
monhé
mono
monstro
monte de merda
mórbido
morcão
mosca morta
mostrengo
mouco
mula
múmia
Nnababo
nabo
não fode nem sai de cima
não tens onde cair morto
narcisista
narigudo
nariz arrebitado
nazi
necrófilo
néscio
nhonhinhas
nhurro
ninfomaníaca
nódoa
nojento
nulidade
Oobcecado
obnóxio
obstinado
obtuso
olhos de carneiro mal morto
onanista
oportunista
ordinário
orelhas de abano
otário
Ppacóvio
padreca
palerma
palhaço
palhaçote
palonça
panasca
paneleiro
panhonhas
panilas
pantomineiro
papa açorda
papagaio
papalvo
paranóico
parasita
pária
parolo
parvalhão
parvo
paspalhão
paspalho
passado
passarão
pata choca
patarata
patego
pateta
patife
patinho feio
pato
pató
pau de virar tripas
pedante
pederasta
pedinchas
pega de empurrão
peida gadoxa
pelintra
pendura
peneirenta
pequeno burguês
pérfido
perliquiteques
pernas de alicate
pés de chumbo
peso morto
pesporrente
petulante
picuinhas
piegas
pilha galinhas
pílulas
pindérica
pinga amor
pintas
pinto calçudo
pintor
piolho
piolhoso
pirata
piroso
pitosga
pobre de espírito
pobretanas
poltrão
popularucho
porcalhão
porco
pote de banhas
preguiçoso
presunçoso
preto
provocador
proxeneta
pulha
punheteiro
putéfia
Qquadrilheira
quatro olhos
quebra bilhas
queixinhas
quezilento
Rrabeta
rabugento
racista
radical
rafeiro
ralé
rameira
rameloso
rancoroso
ranhoso
raquítico
rasca
rascoeira
rasteiro
rata de sacristia
reaccionário
reaças
reles
repelente
ressabiado
retardado
retorcido
ridículo
roto
rufia
rústico
Ssabujo
sacana
sacripanta
sacrista
sádico
safado
safardana
salafrário
saloio
salta pocinhas
sandeu
sapatona
sarnento
sarrafeiro
sebento
seboso
sem classe
sem vergonha
serigaita
sevandija
sicofanta
simplório
snob
soba
sodomita
soez
somítico
sonsa
sórdido
sorna
sovina
suíno
sujo
Ttacanho
tagarela
tanso
tarado
taralhouca
tavolageiro
teimoso
tinhoso
tísico
títere
toleirão
tolo
tonto
torpe
tosco
totó
trabeculoso
trafulha
traiçoeiro
traidor
trambolho
trapaceiro
trapalhão
traste
tratante
trauliteiro
tresloucado
trinca espinhas
trique lariques
triste
troca tintas
troglodita
trombalazanas
trombeiro
trombudo
trouxa
Uunhas de fome
untuoso
urso
Vvaca gorda
vadio
vagabundo
vaidoso
valdevinos
vândalo
velhaco
velhadas
vendido
verme
vesgo
víbora
viciado
vigarista
vígaro
vil
vilão
vingativo
vira casacas
Xxenófobo
Xé xé
xico esperto
Zarolho
zé ninguém
zelota
zero à esquerda
Cacete
Puta
Viado
Foder
Puto
Viadinho
Safado
Fode
Merda
Porra
Caralho
Bosta
Corno
Foda se
Mamona
Sexo
Tití
Virgem
Virgulha
Grande Bunda
Pintinho
Macumba
Putinha
Rapaz de merda
Semen
Sereia
Sereno
Sexy
Shit
Cabaço
Cuzona
Cú
Cu
pica
piquinhas`
        palavrasOfensivas = new Set(palavras.split('\n').map(palavra => palavra.toLowerCase().trim()));
        // Separa as palavras com base em quebras de linha ou outros delimitadores
    } catch (error) {
        console.error(error);
        palavrasOfensivas = [];
    }
}

function verificaComentario(comentario) {
    comentario = removeNumerosComoLetras(comentario.trim());

    // Expressões regulares para dividir o comentário em palavras
    const tokens = comentario.toLowerCase().match(/\b\w+\b/g) || [];
    const lemas = tokens.map(token => token.toLowerCase()); // Aqui você poderia aplicar lematização se necessário

    for (const palavra of palavrasOfensivas) {
        if (tokens.includes(palavra) || comentario.includes(palavra) || lemas.includes(palavra)) {
            return false;
        }
    }
    return true;
}

function removeNumerosComoLetras(texto) {
    // Mapeamento de números para letras
    const mapeamento = {
        '0': 'o',
        '1': 'i',
        '!': 'i',
        '3': 'e',
        '4': 'a',
        '5': 's',
        '7': 't',
    };

    // Substitui os números pelos caracteres correspondentes
    for (const numero in mapeamento) {
        const letra = mapeamento[numero];
        const regex = new RegExp(numero, 'g');
        texto = texto.replace(regex, letra);
    }

    return texto;
}

getPalavrasOfensivas();