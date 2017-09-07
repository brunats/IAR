    //****************************************************************************
    // This program is free software: you can redistribute it and/or modify
    // it under the terms of the GNU General Public License as published by
    // the Free Software Foundation, either version 3 of the License, or
    // (at your option) any later version.
    //
    // This program is distributed in the hope that it will be useful,
    // but WITHOUT ANY WARRANTY; without even the implied warranty of
    // MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    // GNU General Public License for more details.
    //
    // You should have received a copy of the GNU General Public License
    // along with this program.  If not, see <http://www.gnu.org/licenses/>.
    //****************************************************************************
    // Autores:
    //     Bruna Tavares Silva @brunats
    //     Christopher Renkavieski @
    // Disciplina:
    //     Inteligência Artificial - BCC  - CCT UDESC
    // Profº:
    //     Rafael Parpinelli
    //****************************************************************************

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <math.h>

#define ALPHA 0.12
#define K1 1.0
#define K2 1.0
//#define MAX 68.0


    //****************************************************************************
    // Compile
    // $ gcc -Wall formiga_app2.c -o formiga -lm
    // $ ./formiga
    //
    // Instruções:
    //     "param_app.txt" contém os parâmetros mutáveis do sistema
    //         X: tam em X
    //         Y: tam em Y
    //         A: n de agentes
    //         R: raio de visao do agente
    //         P: n max de passos
    //****************************************************************************


typedef struct {
    int posx, posy;
    char movx, movy; //evitar que sejam ambas zero
    int carregando;
    char viva;
} Formiga;

typedef struct {
    int tamX, tamY;
    int agentes;
    int itens;
    int raio;
    int passos;
} Config;

typedef struct {
    char c;
    int posx;
    int posy;
    char carregado;
    double v[2];
} Item;

typedef struct {
    char c;
    int id;
} Matriz;

//adicionadas novas
void carregaConfig(Config *c);
void limparTela();

// atualizadas/certas
void geraImagem(Matriz **m, int x, int y, int n);

void inicializa(Matriz ***m, int x, int y, int itens, Formiga *f, int agentes, Item *it);
void mostra(Matriz **m, int x, int y);
void criaFormigas(Formiga **f, int agentes, int x, int y);
void move(Formiga *f, int raio, int agentes, Matriz **m, int x, int y, Item *it);
int contarItens(Formiga f, int raio, Matriz **m, int x, int y);
float probPegar(Formiga f, int raio, Matriz **m, int x, int y, Item *it);
float probSoltar(Formiga f, int raio, Matriz **m, int x, int y, Item *it);
void tentaPegar(Formiga *f, int raio, Matriz **m, int x, int y, Item *it);
void tentaSoltar(Formiga *f, int raio, Matriz **m, int x, int y, Item *it);
void verificaAcao(Formiga *f, int raio, Matriz **m, int x, int y, Item *it);
int contaTotalItens(Matriz **m, int x, int y);
void mataFormigas(Formiga *f, int agentes, Matriz **m, Item *it);
int formigaViva(Formiga *f, int agentes);

void criaItens(Item **it, Config *cf);
double distancia(Item i1, Item i2);
double contarDist(Formiga f, int raio, Matriz **m, int x, int y, Item *it);

int mod(int a, int b);

double max;
double maiorDist(Item *it, int itens);

int main(){
    Formiga *f;
    Config c;
    Item *it;
    Matriz **m;

    int i;
    int itensFinal;

    //definições de parâmetros
    carregaConfig(&c);

    srand(time(NULL));
    criaFormigas(&f, c.agentes, c.tamX, c.tamY);
    criaItens(&it, &c);
    inicializa(&m, c.tamX, c.tamY, c.itens, f, c.agentes, it);
    
    max = maiorDist(it, c.itens);
    
    mostra(m, c.tamX, c.tamY);
    
    for(i=0;i<c.passos;i++){
        if(i == 10) // ===: aqui define-se em ql passo irá printar
            geraImagem(m, c.tamX, c.tamY, i);
        //printf("main i: %i\n", i);
        //mostra(m, c.tamX, c.tamY);
        //printf("Passo: %d\r", i);
        move(f, c.raio, c.agentes, m, c.tamX, c.tamY, it);
        //usleep(2e4);
    }
    
    i=0;
    mataFormigas(f, c.agentes, m, it);
    while(formigaViva(f, c.agentes) && i<c.passos){
        move(f, c.raio, c.agentes, m, c.tamX, c.tamY, it);
    	mataFormigas(f, c.agentes, m, it);
        i++;
    }
    if(i>=c.passos){
        printf("algo errado não está certo");
    }
    
    mostra(m, c.tamX, c.tamY);
    
    itensFinal = contaTotalItens(m, c.tamX, c.tamY);
    printf("Itens final: %d\n", itensFinal);
    
    free(f);
    free(m);
    return 0;
}

void geraImagem(Matriz **m, int x, int y, int n){
    char url[] = "imagem_", urlp2[] = ".txt", b[10];
    int i, j;
    FILE *arq;

    //concatena os nomes cm o n do parametro
    sprintf(b, "%i", n);
    strcat(url, b);
    strcat(url, urlp2);

    arq = fopen(url, "w");
    if(arq == NULL)
        printf("Erro, nao foi possivel abrir o arquivo\n");
    else{
        for(i=0;i<x;i++){
            for(j=0;j<y;j++){
                fprintf(arq, "%c", m[i][j].c);
            }
            fprintf(arq, "\n");
        }
        fclose(arq);
    }
}

void carregaConfig(Config *c){
    char url[]="param_app.txt";
    char tipo;
    int valor;
    FILE *arq;
    
    arq = fopen(url, "r");
    if(arq == NULL)
        printf("Erro, nao foi possivel abrir o arquivo\n");
    else{
        while( (fscanf(arq,"%c %i\n", &tipo, &valor)!=EOF)){
            switch(tipo){
                case 'X': c->tamX = valor; break;
                case 'Y': c->tamY = valor; break;
                case 'A': c->agentes = valor; break;
                case 'R': c->raio = valor; break;
                case 'P': c->passos = valor; break;
                default: printf("argumentos incorretos / arquivo corrompido\n"); exit(0);
            }
        }
    }            
    fclose(arq);
}

void limparTela(){
    system("clear");
}

void mostra(Matriz **m, int x, int y){
    int i, j;
    
    for(i=0;i<20;i++){
        printf("\n");
    }
    for(i=0;i<x;i++){
        for(j=0;j<y;j++){
            printf("%c", m[i][j].c);
        }
        printf("\n");
    }
}

void inicializa(Matriz ***m, int x, int y, int itens, Formiga *f, int agentes, Item *it){
    int i, j;
    int px, py;
    
    //aloca matriz de experimento
    *m = (Matriz**)malloc(x*sizeof(Matriz*));
    for(i=0;i<x;i++){
        (*m)[i] = (Matriz*)malloc(y*sizeof(Matriz));
    }
    
    //*it = (Item*)malloc(itens*sizeof(Item));
    
    //inicializa matriz com ' ' (espaços)
    for(i=0;i<x;i++){
        for(j=0;j<y;j++){
            (*m)[i][j].c='.';
            (*m)[i][j].id=-1;
        }
    }
    
    //adiciona de modo aleatório os corpos mortos
    for(i=0;i<itens;i++){
    	do{
    		px = rand()%x;
    		py = rand()%y;
            //printf("a\n");
    	}while((*m)[px][py].id != -1);
    	(*m)[px][py].c = it[i].c;
        (*m)[px][py].id = i;
        it[i].posx = px;
        it[i].posy = py;
        it[i].carregado = 0;
    }

    //adiciona os agentes
    for(i=0;i<agentes;i++){
        //adc na matriz da pos da formiga o símbolo f
        (*m)[f[i].posx][f[i].posy].c = 'f';
    }
}
    
void criaFormigas(Formiga **f, int agentes, int x, int y){
    int i;
    
    //aloca vetor de formigas
    *f = (Formiga*)malloc(agentes*sizeof(Formiga));
    
    //inicializa formigas
    for(i=0;i<agentes;i++){
        (*f)[i].posx = rand()%x; //inicializa posicoes de modo aleatório
        (*f)[i].posy = rand()%y;
        //inicializa as componentes de movimentação, com mov [-1,1]
        //  testa até que pelo menos uma das duas nao seja zero
        do{
            (*f)[i].movx = rand()%3 - 1;
            (*f)[i].movy = rand()%3 - 1;
        }while( ((*f)[i].movx == (*f)[i].movy) && ((*f)[i].movx == 0) );
        (*f)[i].carregando = -1;
        (*f)[i].viva = 1;
    }
}

void criaItens(Item **it, Config *cf){
    char url[]="base2.txt";
	char stringa[20], stringb[20], stringc[20], sn1[20], sn2[20];
    double n1, n2;
    int ni = 0;
    int c;
	char tab;
    FILE *arq;
    
    *it = (Item*)malloc(600*sizeof(Item));
    cf->itens = 600;
    
    arq = fopen(url, "r");
    if(arq == NULL)
        printf("Erro, nao foi possivel abrir o arquivo\n");
    else{
			fscanf(arq, "#%s %s %s\n",stringa, stringb, stringc);
			//printf("%s %s\n",stringa, stringb);
			fscanf(arq, "\n");
			
			while( (fscanf(arq,"%s%c%s%c%d\n", sn1, &tab, sn2, &tab, &c)!=EOF)){
                n1 = atof(sn1);
                n2 = atof(sn2);
                (*it)[ni].v[0] = n1;
                (*it)[ni].v[1] = n2;
                (*it)[ni].c = 96 + c;
                ni++;
        	}
        	
    }            
    fclose(arq);
}
    
void move(Formiga *f, int raio, int agentes, Matriz **m, int x, int y, Item *it){
    int i;
    int p;
    int npx, npy;
    
    //move o conj de agentes por vez
    for(i=0;i<agentes;i++){
        if(f[i].viva == 0){
        	continue;
        }
        
        p = rand()%100;
        //até que a probabilidade seja aceitável <60
        //e as novas posicoes válidas (menores que o max e maiores que zero)
        if(p >= 60){
            //gera-se novas posicoes
            do{
                f[i].movx = rand()%3 - 1;
                f[i].movy = rand()%3 - 1;
            }while( (f[i].movx == f[i].movy) && (f[i].movx == 0) );
        }
        
        //novas posicoes da formiga i
        npx = mod(f[i].posx + f[i].movx, x);
        npy = mod(f[i].posy + f[i].movy, y);
        
        if(m[f[i].posx][f[i].posy].id != -1){
            m[f[i].posx][f[i].posy].c = it[m[f[i].posx][f[i].posy].id].c;
        }
        else{
            m[f[i].posx][f[i].posy].c = '.';
        }       
        
        //atualiza novas posicoes e atualiza o F Carregando f sem carregar
        f[i].posx = npx;
        f[i].posy = npy;
        if(f[i].carregando == -1){
            m[f[i].posx][f[i].posy].c = 'f';
        }
        else{
            m[f[i].posx][f[i].posy].c = 'F';
        }
        
        verificaAcao((f+i), raio, m, x, y, it);
    }
}   

int contarItens(Formiga f, int raio, Matriz **m, int x, int y){
    int i, j;
    int cont = 0;
    int px, py;
    
    //pesquisa pela matriz e pela submatriz composta peo inix, iniy
    // qts corpos tem
    for(i=0;i<=2*raio;i++){
        px = mod(f.posx - raio + i, x);
        for(j=0;j<=2*raio;j++){
            py = mod(f.posy - raio + j, y);
            if(m[px][py].id!=-1){
                cont++;
            }
        }
    }
    
    return cont;
}

double contarDist(Formiga f, int raio, Matriz **m, int x, int y, Item *it){
	int i, j;
	int px, py;
	double dist;
    double soma = 0.0;
	//double menor = 1000.0, maior = -1.0;
    int d2 = (2*raio + 1)*(2*raio + 1) - 1;;
	
	//int cont = 0;
	
	//tratar caso de apenas um item
    
    //pesquisa pela matriz e pela submatriz composta peo inix, iniy
    /*
    for(i=0;i<=2*raio;i++){
        px = mod(f.posx - raio + i, x);
        for(j=0;j<=2*raio;j++){
            py = mod(f.posy - raio + j, y);
            if(m[px][py].id!=-1 && !(px==f.posx && py==f.posy)){
                dist = distancia( it[m[f.posx][f.posy].id], it[m[px][py].id] );
                //printf("%lf\n", dist);
                cont ++;
                
                if(dist > maior){
                	maior = dist;
                }
                if(dist < menor){
                	menor = dist;
                }
                
            }
        }
    }
    
    if(cont == 0){
        return 0.0;
    }
    */
    
    for(i=0;i<=2*raio;i++){
        px = mod(f.posx - raio + i, x);
        for(j=0;j<=2*raio;j++){
            py = mod(f.posy - raio + j, y);
            if(m[px][py].id!=-1 && !(px==f.posx && py==f.posy)){
                //dist = (distancia( it[m[f.posx][f.posy].id], it[m[px][py].id] ) - menor)/(maior-menor);
                if(m[f.posx][f.posy].id != -1){
                    dist = distancia( it[m[f.posx][f.posy].id], it[m[px][py].id] )/max;
                }
                else{
                    dist = distancia( it[f.carregando], it[m[px][py].id] )/max;
                }
                //printf("%lf\n", dist);
                dist = 1.0-(dist/ALPHA);
                if(dist<0.0){
                    return 0.0;
                }
                soma += dist;
                
            }
        }
    }
    soma = soma/(double)d2;
    /*
    if(m[f.posx][f.posy].id == -1){
        printf("wtf\n");
        printf("%lf\n", soma);
        printf("%lf     %lf\n", it[m[f.posx][f.posy].id].v[0], it[m[f.posx][f.posy].id].v[1]);
    }
    */
    //printf("\n");
    //printf("%lf\n", soma);
    //printf("\n");
    //printf("%lf\n", soma);
    if(soma>0){
        return soma;
    }
    else{
        return 0.0;
    }
}

float probPegar(Formiga f, int raio, Matriz **m, int x, int y, Item *it){
    double func;
    float prob;
    
    func = contarDist(f, raio, m, x, y, it);
    
    //qto menos itens por vizinho, maior probabilidade
    prob = pow(K1/(K1 + func), 2);
    
    return prob;
}

float probSoltar(Formiga f, int raio, Matriz **m, int x, int y, Item *it){
    double func;
    float prob;
    
    func = contarDist(f, raio, m, x, y, it);
    
    //qt maior a concentração de itens por vizinhos
    prob = pow(func/(K2 + func), 2);
    
    return prob;
}

void tentaPegar(Formiga *f, int raio, Matriz **m, int x, int y, Item *it){
    double p;
    double probP;
    
    p = (double)rand()/RAND_MAX;
    probP = probPegar(*f, raio, m, x, y, it);
    if(p<probP){
        (*f).carregando = m[(*f).posx][(*f).posy].id;
        
        it[m[(*f).posx][(*f).posy].id].carregado = 1;
        it[m[(*f).posx][(*f).posy].id].posx = -1;
        it[m[(*f).posx][(*f).posy].id].posy = -1;
        
        m[(*f).posx][(*f).posy].id = -1;
    }
}

void tentaSoltar(Formiga *f, int raio, Matriz **m, int x, int y, Item *it){
    double p;
    double probS;
    
    p = (double)rand()/RAND_MAX;
    probS = probSoltar(*f, raio, m, x, y, it);
    if(p<probS){
        m[(*f).posx][(*f).posy].id = (*f).carregando;
        
        it[m[(*f).posx][(*f).posy].id].carregado = 0;
        it[m[(*f).posx][(*f).posy].id].posx = (*f).posx;
        it[m[(*f).posx][(*f).posy].id].posy = (*f).posy;
        
        (*f).carregando = -1;
    }
}

// funcao auxiliar que verifica a ação da formiga a cada passo
void verificaAcao(Formiga *f, int raio, Matriz **m, int x, int y, Item *it){
    if( ((*f).carregando != -1) && (m[(*f).posx][(*f).posy].id == -1) ){
        tentaSoltar(f, raio, m, x, y, it);
    }
    else if( (m[(*f).posx][(*f).posy].id != -1) && ((*f).carregando == -1) ){
        tentaPegar(f, raio, m, x, y, it);
    }
}

int contaTotalItens(Matriz **m, int x, int y){
    int cont = 0;
    int i, j;
    
    for(i=0;i<x;i++){
        for(j=0;j<y;j++){
            if(m[i][j].id!=-1){
                cont++;
            }
        }
    }
    
    return cont;
}

void mataFormigas(Formiga *f, int agentes, Matriz **m, Item *it){
	int i;
	
	for(i=0;i<agentes;i++){
		if(f[i].viva == 0){
			continue;
		}
		if(f[i].carregando == -1){
			f[i].viva = 0;
            if(m[f[i].posx][f[i].posy].id == -1){
                m[f[i].posx][f[i].posy].c = '.';
            }
            else{
                m[f[i].posx][f[i].posy].c = it[m[f[i].posx][f[i].posy].id].c;
            }
		}
	}
	
}

int formigaViva(Formiga *f, int agentes){
	int i;
	
	for(i=0;i<agentes;i++){
		if(f[i].viva == 1){
			return 1;
		}
	}
	
	return 0;
}

int mod(int a, int b){
    int r = a % b;
    return r < 0 ? r + b : r;
}

double distancia(Item i1, Item i2){
	double soma = 0, dist;
	int i;
	
	for(i=0;i<2;i++){
		soma += pow((i1.v[i] - i2.v[i]),2);
	}
	dist = sqrt(soma);
	return dist;
}

double maiorDist(Item *it, int itens){
    int i, j;
    double maiorx = -1.0, menorx = 1000.0;
    double maiory = -1.0, menory = 1000.0;
    double maiordist = -1.0, dist;
    int indice[4];
    
    for(i=0;i<itens;i++){
        if(it[i].v[0]>maiorx){
            maiorx = it[i].v[0];
            indice[0] = i;
        }
        if(it[i].v[0]<menorx){
            menorx = it[i].v[0];
            indice[1] = i;
        }
        if(it[i].v[1]>maiory){
            maiory = it[i].v[1];
            indice[2] = i;
        }
        if(it[i].v[0]<menory){
            menory = it[i].v[1];
            indice[3] = i;
        }
    }
    
    for(i=0;i<4;i++){
        for(j=i+1;j<4;j++){
            dist = distancia(it[indice[i]], it[indice[j]]);
            if(dist > maiordist){
                maiordist = dist;
            }
        }
    }
    
    return maiordist;
}













