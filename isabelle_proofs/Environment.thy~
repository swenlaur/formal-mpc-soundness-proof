theory Environment
  imports Main DataTypes Buffers ParentParty 
begin
record environment =
  env_parent_parties :: "(party_id, parent_party) map"
  env_outgoing_buffers :: "buffer list" (* Leaky Buffer list, actually. *)

(* How do I deal with passed  methods? *)
consts env_call :: "'a environment_scheme \<Rightarrow> port_no \<Rightarrow> msg \<Rightarrow> msg option"

consts env_adv_probe :: "'a environment_scheme \<Rightarrow> msg \<Rightarrow> msg"

definition set_outgoing_buffers :: "'a environment_scheme \<Rightarrow> buffer list \<Rightarrow> 'a environment_scheme" where
"set_outgoing_buffers e bl = e\<lparr> outgoing_buffers := bl \<rparr>"




end
