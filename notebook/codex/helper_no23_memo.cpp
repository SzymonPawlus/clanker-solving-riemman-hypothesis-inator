// Exact residual-only cover decision, independently reconstructed from the
// literal finite set-cover specification. No author solver is used.
#include <algorithm>
#include <bitset>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <unordered_set>
#include <vector>
using Mask=std::bitset<512>;
using Clock=std::chrono::steady_clock;
struct Key { Mask missing; int rows; bool operator==(const Key& b)const {
    return rows==b.rows && missing==b.missing; } };
struct Hash {std::size_t operator()(const Key& k)const {
    return std::hash<Mask>{}(k.missing)^(std::size_t(k.rows)*0x9e3779b9U); }};

int main() {
    int M,slots,exclude2,exclude3,seconds;
    while(std::cin>>M>>slots>>exclude2>>exclude3>>seconds) {
        if(M<2 || M>512 || slots<1 || slots>8 || seconds<=0)return 2;
        auto start=Clock::now();
        std::vector<Mask> masks;std::vector<int> speeds;
        std::unordered_set<Mask> unique;
        Mask full;for(int j=0;j<M;++j)full.set(j);
        for(int w=1;w<M;++w) {
            int h=M/std::gcd(M,w);
            if((exclude2 && h==2)||(exclude3 && h==3))continue;
            Mask b;
            for(int j=0;j<M;++j) {
                int z=w*(15*j+1)%(15*M);
                if(std::min(z,15*M-z)<M)b.set(j);
            }
            if(b.any() && unique.insert(b).second){masks.push_back(b);speeds.push_back(w);}
        }
        std::vector<std::vector<int>> supports(M);
        for(int j=0;j<M;++j)for(int i=0;i<int(masks.size());++i)
            if(masks[i][j])supports[j].push_back(i);
        std::vector<int> priority(M);std::iota(priority.begin(),priority.end(),0);
        std::stable_sort(priority.begin(),priority.end(),[&](int a,int b){
            return supports[a].size()<supports[b].size();});
        std::unordered_set<Key,Hash> failed;
        std::vector<int> answer;
        std::uint64_t nodes=0,hits=0,prunes=0;
        auto solve=[&](auto&& self,const Mask& R,int r)->bool {
            ++nodes;
            if((nodes&1023)==0 &&
               std::chrono::duration<double>(Clock::now()-start).count()>seconds)
                throw std::runtime_error("deadline");
            if(R.none())return true;
            if(!r)return false;
            Key key{R,r};
            if(failed.count(key)){++hits;return false;}
            std::vector<int> gains(masks.size());
            int most=0;std::vector<int> top;
            for(int i=0;i<int(masks.size());++i) {
                gains[i]=(masks[i]&R).count();
                if(gains[i]>gains[most])most=i;
                top.push_back(gains[i]);
            }
            if(!masks.empty() && gains[most]==int(R.count())){
                answer.push_back(speeds[most]);return true;
            }
            std::sort(top.begin(),top.end(),std::greater<int>());
            int bound=0;for(int i=0;i<r && i<int(top.size());++i)bound+=top[i];
            if(bound<int(R.count())){++prunes;failed.insert(key);return false;}
            int pivot=-1;for(int j:priority)if(R[j]){pivot=j;break;}
            auto options=supports[pivot];
            std::stable_sort(options.begin(),options.end(),[&](int a,int b){return gains[a]>gains[b];});
            for(int i:options)if(self(self,R&~masks[i],r-1)) {
                answer.push_back(speeds[i]);return true;
            }
            failed.insert(key);return false;
        };
        bool complete=true,found=false;
        try {found=solve(solve,full,slots);}catch(const std::runtime_error&){complete=false;}
        double elapsed=std::chrono::duration<double>(Clock::now()-start).count();
        std::cout<<M<<' '<<complete<<' '<<found<<' '<<nodes<<' '<<hits<<' '<<prunes
                 <<' '<<failed.size()<<' '<<elapsed<<' '<<answer.size();
        for(int w:answer)std::cout<<' '<<w;
        std::cout<<std::endl;
    }
}
