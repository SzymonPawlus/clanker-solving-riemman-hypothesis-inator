// Literal subset enumeration. No density, period, or greedy-order sieve.
#include <algorithm>
#include <cstdint>
#include <functional>
#include <iostream>
#include <numeric>
#include <vector>
int main() {
    int first,last,r;std::cin>>first>>last>>r;
    if (!std::cin || first<2 || last>60 || first>last || r<1 || r>14) return 2;
    for (int M=first;M<=last;++M) {
        std::vector<std::uint64_t> rows(M);
        const std::uint64_t full=(std::uint64_t(1)<<M)-1;
        for (int w=1;w<M;++w) for (int j=0;j<M;++j) {
            int z=w*(15*j+1)%(15*M);
            if (std::min(z,15*M-z)<M) rows[w]|=std::uint64_t(1)<<j;
        }
        std::uint64_t subsets=0,covered=0,primitive=0,minimal=0;
        std::vector<int> chosen;
        std::function<void(int,std::uint64_t)> walk=[&](int next,std::uint64_t mask) {
            if (int(chosen.size())==r) {
                ++subsets;
                if (mask!=full) return;
                ++covered;
                int g=M;for (int w:chosen) g=std::gcd(g,w);
                if (g!=1) return;
                ++primitive;
                for (int i=0;i<r;++i) {
                    std::uint64_t other=0;
                    for (int j=0;j<r;++j) if(i!=j) other|=rows[chosen[j]];
                    if (other==full) return;
                }
                ++minimal;
                std::cout<<"C "<<M;for(int w:chosen)std::cout<<' '<<w;
                std::cout<<'\n';return;
            }
            int remaining=r-chosen.size();
            for (int w=next;w<=M-remaining;++w) {
                chosen.push_back(w);walk(w+1,mask|rows[w]);chosen.pop_back();
            }
        };
        walk(1,0);
        std::cout<<"S "<<M<<' '<<subsets<<' '<<covered<<' '<<primitive<<' '<<minimal<<'\n';
    }
}
