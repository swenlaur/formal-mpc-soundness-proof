theory Functionality
  imports 
    Main 
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/basic_model/ProtocolParty"
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/data_types/DataTypes"
begin

(* I should only instantiate fnl_is_env = false with std fnl *)
record functionality =
  fnl_outgoing_buffers :: "msg list list"
  fnl_is_env :: bool

consts fnl_call :: "'a functionality_scheme \<Rightarrow> functionality_id \<Rightarrow> msg \<Rightarrow> msg option"

consts fnl_adv_probe :: "'a functionality_scheme \<Rightarrow> msg \<Rightarrow> msg"
(* võiks saata write_instructioneid *)

definition set_outgoing_buffers :: 
"'a functionality_scheme \<Rightarrow> msg list list \<Rightarrow> 'a functionality_scheme" where
"set_outgoing_buffers f bl = f\<lparr>fnl_outgoing_buffers := bl\<rparr>"

(* StandardFunctionality.__call__ *)
consts fnl_update :: 
"'a functionality_scheme option => party_id \<Rightarrow> msg \<Rightarrow> 'a functionality_scheme"






end
