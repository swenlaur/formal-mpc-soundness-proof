theory StandardFunctionality
  imports 
    Main 
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/network_components/Functionality"
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/data_types/DataTypes"
begin

typedecl sharing_module
typedecl computation_module
typedecl reconstruction_module
typedecl func_data

record standard_functionality = functionality +
  fnl_sharing_module :: sharing_module
  fnl_computation_module :: computation_module
  fnl_reconstruction_module :: reconstruction_module

consts func_call :: "'a standard_functionality_scheme \<Rightarrow> 'a standard_functionality_scheme"

end