import Std

namespace SupportSaturation
variable {Point Lit : Type}
def Models (holds : Point → Lit → Prop) (term : Lit → Prop) (p : Point) :=
  ∀ l, term l → holds p l
def Saturate (holds : Point → Lit → Prop) (S : Point → Prop) (l : Lit) :=
  ∀ p, S p → holds p l

/-- Weight and positive witnesses are evaluated on the listed support.
Entailment of the observation is tested over every valuation. -/
theorem better_iff_saturation (holds : Point → Lit → Prop)
    (support theory observation : Point → Prop) (heavy : (Point → Prop) → Prop)
    (mono : ∀ A B : Point → Prop, (∀ p, A p → B p) → heavy A → heavy B) :
    (∃ t, heavy (fun p => support p ∧ Models holds t p) ∧
       (∃ p, support p ∧ Models holds t p ∧ theory p) ∧
       ∀ p, theory p → Models holds t p → observation p) ↔
    ∃ S, (∀ p, S p → support p) ∧ heavy S ∧ (∃ p, S p ∧ theory p) ∧
       ∀ p, theory p → Models holds (Saturate holds S) p → observation p := by
  constructor
  · rintro ⟨t, wt, ⟨v, hv, hvt, hth⟩, entails⟩
    refine ⟨fun p => support p ∧ Models holds t p, fun _ h => h.1, wt,
      ⟨v, ⟨hv, hvt⟩, hth⟩, ?_⟩
    intro p hp hs
    exact entails p hp (fun l hl => hs l (fun _ hq => hq.2 _ hl))
  · rintro ⟨S, sub, wt, ⟨v, hv, hth⟩, entails⟩
    refine ⟨Saturate holds S, mono _ _ (fun p hp => ⟨sub p hp, fun _ hl => hl p hp⟩) wt,
      ⟨v, sub v hv, fun _ hl => hl v hv, hth⟩, entails⟩
#print axioms better_iff_saturation
end SupportSaturation
