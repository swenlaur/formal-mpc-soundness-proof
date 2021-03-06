theory Functionality
  imports 
    Main 
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/basic_model/ProtocolParty"
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/data_types/DataTypes"
begin

(* I should only instantiate fnl_is_env = false with std fnl *)
typedecl env_state
typedecl func_state

record functionality =
  fnl_outgoing_buffers :: "msg list list"
  fnl_is_env :: bool
  fnl_state :: func_state

consts fnl_call :: "'a functionality_scheme \<Rightarrow> functionality_id \<Rightarrow> msg \<Rightarrow> msg option"

consts fnl_adv_probe :: "'a functionality_scheme \<Rightarrow> msg \<Rightarrow> msg * write_instructions"
(* võiks saata write_instructioneid *)

consts invoke_environment :: "'a functionality_scheme \<Rightarrow> msg \<Rightarrow> msg * write_instructions"


definition set_outgoing_buffers :: 
"'a functionality_scheme \<Rightarrow> msg list list \<Rightarrow> 'a functionality_scheme" where
"set_outgoing_buffers f bl = f\<lparr>fnl_outgoing_buffers := bl\<rparr>"


definition fnl_eval_write_instructions ::
"'a functionality_scheme \<Rightarrow> (functionality_id \<times> msg) list \<Rightarrow> 'a functionality_scheme" where
"fnl_do_write_instructions f w = f\<lparr>fnl_outgoing_buffers := (update_outgoing_buffers (fnl_outgoing_buffers f) w)\<rparr>"

(* StandardFunctionality.__call__ *)
consts fnl_update :: 
"'a functionality_scheme option => party_id \<Rightarrow> msg \<Rightarrow> 'a functionality_scheme"






end
