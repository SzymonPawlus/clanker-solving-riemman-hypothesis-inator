// Numerical probe only. Exact strict masks at one maximal anchor, threshold1/15.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
int main(int argc,char**argv){
 int begin=argc>1?std::atoi(argv[1]):100,end=argc>2?std::atoi(argv[2]):1200;
 uint64_t pairs=0;
 for(int M=begin;M<=end;++M){
  int words=(M+63)/64;
  std::vector<std::vector<uint64_t>> B(M,std::vector<uint64_t>(words));
  for(int w=1;w<M;++w)for(int j=0;j<M;++j){
   int s=(int)((int64_t)w*(15*j+1)%(15*M));
   if(std::min(s,15*M-s)<M)B[w][j/64]|=1ULL<<(j%64);
  }
  int best=M,bu=0,bw=0;
  for(int u=1;14*u<M;++u)for(int w=u+1;w<M;++w){
   int hits=0;++pairs;
   for(int b=0;b<words;++b)hits+=__builtin_popcountll(B[u][b]&B[w][b]);
   if(hits<best){best=hits;bu=u;bw=w;}
  }
  if(best<(M-1)/105){std::cout<<"COUNTEREXAMPLE "<<M<<' '<<bu<<' '<<bw<<' '<<best<<' '<<(M-1)/105<<'\n';return 0;}
  if(M%100==0||M==end)std::cout<<"PASS "<<M<<" min "<<best<<" pair "<<bu<<','<<bw<<" checked "<<pairs<<std::endl;
 }
}
