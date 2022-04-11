theory ProtocolParty
imports Main DataTypes AdversarialAction StatefulInterpreter
begin

record protocol_party =
  corrupted :: bool (* Can we have a default False here like in the Python code? *)
  partyInterpreter :: stateful_interpreter



(* ==== HELPERS START HERE ===== *)

(* takes a party and gives a corrupted party *)
definition set_corrupted :: "'a protocol_party_scheme \<Rightarrow> 'a protocol_party_scheme" where
"set_corrupted p = p\<lparr>corrupted :=  True\<rparr>"


(* an undefined function that takes a party and gives its internals *)
consts dump_internals :: 
"'a protocol_party_scheme \<Rightarrow> state \<times> public_param \<times> private_param"
(*
 definition dump_internals :: "'a protocol_party_scheme \<Rightarrow> state \<times> public_param \<times> private_param" where
"dump_internals p = "
*)


(* 
Replies with None if party is not corrupted
 or the state+parameters if party is corrupted.
*)
definition corruption_reply :: 
"'a protocol_party_scheme \<Rightarrow> (state \<times> public_param \<times> private_param) option" where
"corruption_reply p = (if corrupted p then Some (dump_internals p) else None)"

(* ==== HELPERS END HERE ===== *)

(* takes a party, corrupts it, updates the map,  *)
definition corrupt_party :: "'a protocol_party_scheme \<Rightarrow> adv_input" where



end