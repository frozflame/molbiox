#include<stdio.h>
#include<stdint.h>
#define KSIZE 4


#define GLOBAL  1
#define OVERLAP 2
#define LOCAL   3

typedef int16_t shortType;
typedef int64_t scoreType;
typedef int64_t indexType;


inline scoreType max2(scoreType a, scoreType b) {
    return a > b ? a : b;
    }

inline scoreType max3(scoreType a, scoreType b, scoreType c) {
    return max2(a,b) < c ?  c : max2(a,b);
    }

inline scoreType* idx( scoreType* matr,
    indexType i, indexType j, indexType k, indexType isize, indexType jsize){
        return matr + i*jsize*KSIZE + j*KSIZE + k;
    }


void build(scoreType* matr, indexType isize, indexType jsize,
    scoreType rho, scoreType sigma, shortType scheme){


    /*
        Intro to Bioinfo Algorithms, P184
        set the score for a gap of length x to be −(rho + sigma * x), where rho > 0

    */

    scoreType score;
    scoreType trace;
    indexType i, j;

    for(i = 1; i < isize; i++)
    for(j = 1; j < jsize; j++)
    {

        /* i - 1 */
        *idx(matr, i, j, 0, isize, jsize) = max2(
            *idx(matr, i-1, j, 0, isize, jsize) - sigma,
            *idx(matr, i-1, j, 2, isize, jsize) - sigma - rho
        );

        /* j - 1 */
        *idx(matr, i, j, 1, isize, jsize) = max2(
            *idx(matr, i, j-1, 1, isize, jsize) - sigma,
            *idx(matr, i, j-1, 2, isize, jsize) - sigma - rho
        );

        /* i - 1 and j - 1 */
        score = max3(
            *idx(matr, i, j, 0, isize, jsize),
            *idx(matr, i, j, 1, isize, jsize),
            *idx(matr, i, j, 2, isize, jsize)
                + *idx(matr, i-1, j-1, 2, isize, jsize)
        );

        if (score < 0 && scheme == LOCAL) score = 0;
        *idx(matr, i, j, 2, isize, jsize) = score;

        /* set traces */
        if      (score == *idx(matr, i, j, 0, isize, jsize)) trace = 0;
        else if (score == *idx(matr, i, j, 1, isize, jsize)) trace = 1;
        else if (score == *idx(matr, i, j, 2, isize, jsize)) trace = 2;

        *idx(matr, i, j, 3, isize, jsize) = trace;
    }
}


indexType backtrack(scoreType* matr, indexType isize,  indexType jsize,
                                indexType istart, indexType jstart,
                                indexType* iarr,  indexType* jarr,
                                shortType scheme){

    indexType i;
    indexType j;
    indexType x;
    indexType indel_code;
    scoreType trace;

    /* a not-used index number for indel */
    //    indel_code = max2(isize, jsize) + 1;
    indel_code = 0;

    i = istart;
    j = jstart;
    x = 0;

//    scoreType scores[3];

    while ( (i&&j) || (scheme == GLOBAL && (i||j)) ){

//        printf("back 1: %i, %i, %i, ", i, j, x);

        iarr[x] = i;
        jarr[x] = j;
        trace = *idx(matr, i, j, 3, isize, jsize);

        /* last 2 bits */
        if      ((trace & 3) == 0) { iarr[x] = i; jarr[x] = indel_code; i--; }
        else if ((trace & 3) == 1) { jarr[x] = j; iarr[x] = indel_code; j--; }
        else if ((trace & 3) == 2) { iarr[x] = i; jarr[x] = j; i--; j--; }
        else break;

//        printf("back 2: %i \n", trace & 3);

        x++;
    }
    return x;
}

int test(int* matr){
    matr[0] += 1;
    return 1;
}

