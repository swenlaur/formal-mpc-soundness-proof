theory ProtocolParty
imports Main DataTypes AdversarialAction StatefulInterpreter
begin

record protocol_party =
  corrupted :: bool
  partyInterpreter :: stateful_interpreter


(* returns a corrupted party *)
definition set_corrupted :: "'a protocol_party_scheme \<Rightarrow> 'a protocol_party_scheme" where
"set_corrupted p = p\<lparr>corrupted :=  True\<rparr>"

(* an undefined function that takes a party and gives its internals *)
consts internal_state :: 
"'a protocol_party_scheme \<Rightarrow> state \<times> public_param \<times> private_param"
(*
 definition internal_state :: "'a protocol_party_scheme \<Rightarrow> state \<times> public_param \<times> private_param" where
"dump_internals p = "
*)

(* 
Replies with None if party is not corrupted
 or the state+parameters if party is corrupted.
*)
definition corruption_reply :: 
"'a protocol_party_scheme \<Rightarrow> (state \<times> public_param \<times> private_param) option" where
"corruption_reply p = (if corrupted p then Some (internal_state p) else None)"


end