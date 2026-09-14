// Independent direct-residue finite audit of the smallest-period<=16 claim.
// Emits exact top-six charges for every distinct base; Python sums rationals.
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <numeric>
#include <set>
#include <vector>
using namespace std;
struct Row {int h,a;vector<int>B;};
struct Charge {long long num,den;int h,a;};
bool less_charge(const Charge&x,const Charge&y){
 return (__int128)x.num*y.den<(__int128)y.num*x.den;
}
int main(){
 vector<Row> rows;
 for(int h=2;h<=300;h++){
  set<vector<int>>seen;
  for(int a=1;a<h;a++)if(gcd(a,h)==1){
   vector<int>B;
   for(int j=0;j<h;j++){
    int residue=a*(15*j+1)%(15*h);
    if(residue<h || residue>14*h)B.push_back(j);
   }
   if(!B.empty() && seen.insert(B).second)rows.push_back({h,a,B});
  }
 }
 long long comparisons=0;
 int bases=0;
 for(size_t index=0;index<rows.size();index++){
  const Row&base=rows[index];
  int p=base.h,b=base.B.size();
  if(p<17 || p>91)continue;
  bases++;
  vector<vector<int>>hist(p+1);
  for(int d=1;d<=p;d++)if(p%d==0){
   hist[d].assign(d,0);
   for(int r:base.B)hist[d][r%d]++;
  }
  Charge rawtail={41,301,0,0};
  Charge conditioned={2LL*(p-b)*301+1LL*p*(13+15*b),15LL*p*301,0,0};
  Charge tail=less_charge(rawtail,conditioned)?rawtail:conditioned;
  array<Charge,6>best;best.fill(tail);
  for(size_t i=0;i<rows.size();i++){
   const Row&candidate=rows[i];
   if(candidate.h<p || i==index)continue;
   comparisons++;
   int h=candidate.h,d=gcd(p,h),dot=0;
   for(int r:candidate.B)dot+=hist[d][r%d];
   Charge C={1LL*p*static_cast<int>(candidate.B.size())-1LL*d*dot,1LL*p*h,h,candidate.a};
   if(less_charge(best[0],C)){
    best[0]=C;
    sort(best.begin(),best.end(),less_charge);
   }
  }
  cout<<p<<' '<<base.a<<' '<<b;
  for(int r:base.B)cout<<' '<<r;
  for(const auto&C:best)cout<<' '<<C.h<<' '<<C.a<<' '<<C.num<<' '<<C.den;
  cout<<'\n';
 }
 cerr<<"distinct_rows "<<rows.size()<<" bases "<<bases
     <<" comparisons "<<comparisons<<'\n';
}
