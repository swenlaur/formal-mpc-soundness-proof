theory StandardFunctionality
  imports Main DataTypes Buffers 
begin

typedecl sharing_module
typedecl computation_module
typedecl reconstruction_module

record standard_functionality =
  fnl_sharing_module :: sharing_module
  fnl_computation_module :: computation_module
  fnl_reconstruction_module :: reconstruction_module

(* pass for now  *)
consts fnl_adv_probe :: "'a standard_functionality_scheme \<Rightarrow> msg \<Rightarrow> msg"
end