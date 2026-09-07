import Verified.Woodall.Basic
import Verified.Woodall.Instances

open Verified.Woodall

-- ============ ROW-BY-ROW #check ============
#check @Verified.Woodall.length_le_card_deltaOut
#check @Verified.Woodall.length_le_tau
#check @Verified.Woodall.length_le_countP
#check @Verified.Woodall.countP_erase_of_mem
#check @Verified.Woodall.mem_allVertexSets
#check @Verified.Woodall.nonempty_and_proper_of_isDicutShore
#check @Verified.Woodall.one_le_card_deltaOut
#check @Verified.Woodall.not_isMinDicutSize_zero
#check @Verified.Woodall.isMinDicutSize_unique
#check @Verified.Woodall.IsDijoin.mono
#check @Verified.Woodall.isDijoin_all
#check @Verified.Woodall.woodall_of_isMinDicutSize_one
#check @Verified.Woodall.woodall_of_isMinDicutSize_le_one
#check @Verified.Woodall.isDicutShoreAllowingEmpty_of_isDicutShore
#check @Verified.Woodall.cycle3_no_dicut
#check @Verified.Woodall.cycle3_no_min_dicut_size
#check @Verified.Woodall.cycle3_tau
#check @Verified.Woodall.cycle3_empty_isDijoin
#check @Verified.Woodall.cycle3_trap
#check @Verified.Woodall.path3_dicutShores
#check @Verified.Woodall.path3_tau
#check @Verified.Woodall.path3_tau?
#check @Verified.Woodall.diamond_tau
#check @Verified.Woodall.diamond_tau?
#check @Verified.Woodall.diamondJ₁_isDijoin
#check @Verified.Woodall.diamondJ₂_isDijoin
#check @Verified.Woodall.diamond_disjoint
#check @Verified.Woodall.diamond_partition
#check @Verified.Woodall.diamond_two_le_tau
#check @Verified.Woodall.nearMiss_tau
#check @Verified.Woodall.nearMiss_tau?
#check @Verified.Woodall.nearMiss_shore
#check @Verified.Woodall.nearMiss_all_isDijoin
#check @Verified.Woodall.nearMiss_two_sources
#check @Verified.Woodall.twoArcs_conventions_disagree
#check @Verified.Woodall.twoArcs_tau
#check @Verified.Woodall.twoArcs_woodall
#check @Verified.Woodall.path3_woodall
#check @Verified.Woodall.nearMiss_woodall
#check @Verified.Woodall.WoodallConjecture
-- supporting bridge lemmas the rows lean on
#check @Verified.Woodall.tau?_eq_some_iff
#check @Verified.Woodall.tau?_eq_none_iff
#check @Verified.Woodall.tau?_eq_none_iff_not_exists
#check @Verified.Woodall.not_isMinDicutSize_of_no_dicut
#check @Verified.Woodall.mem_dicutShores
#check @Verified.Woodall.IsDicutShore
#check @Verified.Woodall.IsDijoin
#check @Verified.Woodall.IsMinDicutSize
#check @Verified.Woodall.IsArcPartition
#check @Verified.Woodall.deltaOut
#check @Verified.Woodall.deltaIn

-- ============ #print axioms ============
#print axioms Verified.Woodall.length_le_card_deltaOut
#print axioms Verified.Woodall.length_le_tau
#print axioms Verified.Woodall.length_le_countP
#print axioms Verified.Woodall.countP_erase_of_mem
#print axioms Verified.Woodall.mem_allVertexSets
#print axioms Verified.Woodall.nonempty_and_proper_of_isDicutShore
#print axioms Verified.Woodall.one_le_card_deltaOut
#print axioms Verified.Woodall.not_isMinDicutSize_zero
#print axioms Verified.Woodall.isMinDicutSize_unique
#print axioms Verified.Woodall.IsDijoin.mono
#print axioms Verified.Woodall.isDijoin_all
#print axioms Verified.Woodall.woodall_of_isMinDicutSize_one
#print axioms Verified.Woodall.woodall_of_isMinDicutSize_le_one
#print axioms Verified.Woodall.isDicutShoreAllowingEmpty_of_isDicutShore
#print axioms Verified.Woodall.cycle3_no_dicut
#print axioms Verified.Woodall.cycle3_no_min_dicut_size
#print axioms Verified.Woodall.cycle3_tau
#print axioms Verified.Woodall.cycle3_empty_isDijoin
#print axioms Verified.Woodall.cycle3_trap
#print axioms Verified.Woodall.path3_dicutShores
#print axioms Verified.Woodall.path3_tau
#print axioms Verified.Woodall.path3_tau?
#print axioms Verified.Woodall.diamond_tau
#print axioms Verified.Woodall.diamond_tau?
#print axioms Verified.Woodall.diamondJ₁_isDijoin
#print axioms Verified.Woodall.diamondJ₂_isDijoin
#print axioms Verified.Woodall.diamond_disjoint
#print axioms Verified.Woodall.diamond_partition
#print axioms Verified.Woodall.diamond_two_le_tau
#print axioms Verified.Woodall.nearMiss_tau
#print axioms Verified.Woodall.nearMiss_tau?
#print axioms Verified.Woodall.nearMiss_shore
#print axioms Verified.Woodall.nearMiss_all_isDijoin
#print axioms Verified.Woodall.nearMiss_two_sources
#print axioms Verified.Woodall.twoArcs_conventions_disagree
#print axioms Verified.Woodall.twoArcs_tau
#print axioms Verified.Woodall.twoArcs_woodall
#print axioms Verified.Woodall.path3_woodall
#print axioms Verified.Woodall.nearMiss_woodall
#print axioms Verified.Woodall.tau?_eq_some_iff
#print axioms Verified.Woodall.tau?_eq_none_iff
#print axioms Verified.Woodall.tau?_eq_none_iff_not_exists
