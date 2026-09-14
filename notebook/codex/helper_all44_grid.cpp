// Independent literal integer-grid kernel for the normalized 44-core data.
// Python validates all input bounds before calling this program. No author
// certificate generator or author checker is imported or translated here.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <set>
#include <vector>
using I = std::int64_t;
using W = __int128_t;
struct Atom { I a, b, z; };

I count(I n, I q, const Atom& x) {
    const W modulus = W(n)*x.b;
    I hits = 0;
    for (I k=0; k<n; ++k) {
        W residue = (W(q)*(W(k)*x.b+x.a)) % modulus;
        if (15*std::min(residue,modulus-residue) < modulus) ++hits;
    }
    return hits;
}

int main() {
    I M,D,A; std::cin >> M >> D >> A;
    std::set<I> core;
    for (int i=0; i<8; ++i) { I v; std::cin >> v; core.insert(v); }
    std::vector<Atom> atoms(A);
    for (auto& x: atoms) std::cin >> x.a >> x.b >> x.z;
    if (!std::cin || M<=0 || D<=0 || A<=0) return 2;
    if (count(1,1,{1,15,1}) || count(1,1,{14,15,1}) ||
        count(1,1,{0,1,1})!=1) return 3;
    I columns=0, maxnum=0, maxden=1, maxn=0, maxq=0;
    std::vector<std::pair<I,I>> maximizers;
    for (I n=1; n<=30; ++n) {
        for (I q=1; q<M*n; ++q) {
            if (std::gcd(n,q)!=1 || (n==1 && core.count(q))) continue;
            I numerator=0;
            for (auto x:atoms) numerator += x.z*count(n,q,x);
            I denominator=n*D;
            if (numerator>denominator) {
                std::cerr << "FAIL " << n << ' ' << q << ' ' << numerator
                          << '/' << denominator << '\n'; return 4;
            }
            W compare = W(numerator)*maxden-W(maxnum)*denominator;
            if (compare>0) {
                maxnum=numerator; maxden=denominator; maxn=n; maxq=q;
                maximizers.clear();
            }
            if (compare>=0) maximizers.emplace_back(n,q);
            ++columns;
        }
    }
    I lifted=0;
    for (I c=1; c<=10; ++c) {
        for (I w=1; w<M*c; ++w) {
            if (w%c==0 && core.count(w/c)) continue;
            I g=std::gcd(c,w), n=c/g, q=w/g;
            I direct=0,reduced=0;
            for (auto x:atoms) {
                direct += x.z*count(c,w,x);
                reduced += x.z*count(n,q,x);
            }
            if (W(direct)*n!=W(reduced)*c || direct>c*D) return 5;
            ++lifted;
        }
    }
    std::cout << columns << ' ' << maxnum << ' ' << maxden << ' '
              << lifted << ' ' << maximizers.size();
    for (auto [n,q]:maximizers) std::cout << ' ' << n << ' ' << q;
    std::cout << '\n';
}
