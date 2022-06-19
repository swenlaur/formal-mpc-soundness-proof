theory Environment
  imports 
    Main 
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/data_types/DataTypes"
begin
record environment =
  env_outgoing_buffers :: "msg list list" 

(* I deprecated port number, but it might not make sense here if env also talks to non functionalities *)
consts env_call :: "'a environment_scheme \<Rightarrow> functionality_id \<Rightarrow> msg \<Rightarrow> msg option"

consts env_adv_probe :: "'a environment_scheme \<Rightarrow> msg \<Rightarrow> msg"

definition set_outgoing_buffers :: "'a environment_scheme \<Rightarrow> msg list list \<Rightarrow> 'a environment_scheme" where
"set_outgoing_buffers e bl = e\<lparr> env_outgoing_buffers := bl \<rparr>"

end