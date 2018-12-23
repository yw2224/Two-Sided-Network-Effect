#include <stdio.h>
#include <algorithm>
#include <cstdlib>
#include <iostream>
#define ONE (double)(1)
#define INF 1e+100
#define X 100
#define Y 500
#define Z 500
#define array(a,x,y,z) a[(x)*Y*Z+(y)*Z+(z)]

double dp[X*Y*Z], pm[X*Y*Z], pn[X*Y*Z];
int prevn[X*Y*Z], prevm[X*Y*Z];
int a, b, scale, depth, bestm, bestn;
double t, p, q, bestp, bestq;

void printbest(int l, int m, int n, double p, double q)
{
	if (l == 0) return;
	printbest(l - 1, array(prevm,l,m,n), array(prevn,l,m,n), array(pm,l,m,n), array(pn,l,m,n));
	printf("Day %d: m = %.8lf, n = %.8lf, p = %.8lf, q = %.8lf.\n", l, m * ONE / scale, n * ONE / scale, p, q);
}

int main()
{
	printf("Input a, b, scale and depth (recommended scale = 50 or 100, depth = 20).\n");
	scanf("%d%d%d%d", &a, &b, &scale, &depth);
	for (int m = 0; m <= scale; m++)
		for (int n = 0; n <= scale; n++)
			array(dp,0,m,n) = -INF;
	array(dp,0,0,0) = 0;
	for (int l = 1; l <= depth; l++) {
		printf("Calculating step %d\n", l);
		for (int m = 0; m <= scale; m++)
			for (int n = 0; n <= scale; n++) {
				array(dp,l,m,n) = 0;
				for (int mm = 0; mm <= scale; mm++)
					for (int nn = 0; nn <= scale; nn++) {
						if(mm > m || nn > n) continue;
						p = (ONE - m * ONE / scale) * (1 + a * nn * nn * ONE / scale / scale);
						q = (ONE - n * ONE / scale) * (1 + b * mm * mm * ONE / scale / scale);
						if (p < 0 || p > 1 || q < 0 || q > 1)
							continue;

						t = array(dp,l-1,mm,nn) + p * (m - mm) / scale + q * (n - nn) / scale;
						if (t > array(dp,l,m,n)) {
							array(dp,l,m,n) = t;
							array(prevm,l,m,n) = mm;
							array(prevn,l,m,n) = nn;
							array(pm,l,m,n) = p;
							array(pn,l,m,n) = q;
						}
					}
			}
	}
	t = 0;
	for (int m = 0; m <= scale; m++)
		for (int n = 0; n <= scale; n++)
			if (array(dp,depth,m,n) > t) {
				t = array(dp,depth,m,n);
				bestm = m;
				bestn = n;
				bestp = array(pm,depth,m,n);
				bestq = array(pn,depth,m,n);
			}
	printf("Max profit = %.8lf.\n", t);
	printbest(depth, bestm, bestn, bestp, bestq);
	return 0;
}