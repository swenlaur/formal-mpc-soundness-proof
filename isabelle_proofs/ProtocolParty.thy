theory ProtocolParty
imports Main DataTypes StatefulInterpreter Buffers
begin

record protocol_party =
  party_interpreter :: stateful_interpreter
  party_incoming_buffers :: "(functionality_id, msg list) map"
  party_outgoing_buffers :: "(functionality_id, msg list) map"

(* an undefined function that takes a party and gives its internals *)
consts internal_state :: 
"'a protocol_party_scheme \<Rightarrow> state \<times> public_param \<times> private_param"


(* Helper list methods *)
fun fst_unzip :: "('a \<times> 'b) list \<Rightarrow> 'a list" where
  "fst_unzip [] = []" |
  "fst_unzip ((a,b) # xs) = a # fst_unzip xs"

fun snd_unzip :: "('a \<times> 'b) list \<Rightarrow> 'b list" where
  "snd_unzip [] = []" |
  "snd_unzip ((a,b) # xs) = b # snd_unzip xs"

primrec remove_nth :: "nat => 'a list \<Rightarrow> 'a list" where
"remove_nth n [] = []" |
"remove_nth n (x # xs) = (case n of 0 \<Rightarrow> xs | Suc m \<Rightarrow> x # remove_nth m xs)"


(* Buffer methods *)
definition buffer_with_msg ::
"(functionality_id, msg list) map \<Rightarrow> (functionality_id \<times> msg) \<Rightarrow> msg list list" where
"buffer_with_msg bs w = 
  (let f=fst w in
  (let m=snd w in
  (case bs f of 
    None \<Rightarrow> [] |
    Some b \<Rightarrow>  [m # b])))" 

definition update_outgoing_buffers :: (* [] should be a msg list list... *)
"(functionality_id, msg list) map \<Rightarrow> (functionality_id \<times> msg) list \<Rightarrow> (functionality_id, msg list) map" where
"update_outgoing_buffers bs ws = (map_upds bs (fst_unzip ws) [])"

definition clock_message ::
"'a protocol_party_scheme \<Rightarrow> functionality_id \<Rightarrow> nat \<Rightarrow> msg option \<times> 'a protocol_party_scheme" where
"clock_message p f n = 
  (case party_incoming_buffers p f of
    None \<Rightarrow> (None, p) |
    Some b \<Rightarrow> if n \<ge> length b then (None, p) 
      else (Some (b ! n), p\<lparr>party_incoming_buffers := (map_upds (party_incoming_buffers p) [f] [remove_nth n b])\<rparr>))"

definition empty_incoming_buffer :: 
"'a protocol_party_scheme \<Rightarrow> functionality_id \<Rightarrow> bool" where
"empty_incoming_buffer p f =
  (case party_incoming_buffers p f of
    None => True |
    Some b => if b=[] then True else False)"

consts peek_message ::
"'a protocol_party_scheme \<Rightarrow> functionality_id \<Rightarrow> msg_index \<Rightarrow> msg"

(* Party methods *)
definition do_write_instructions ::
"'a protocol_party_scheme \<Rightarrow> (functionality_id \<times> msg) list \<Rightarrow> 'a protocol_party_scheme" where
"do_write_instructions p w = p\<lparr>party_outgoing_buffers := (update_outgoing_buffers (party_outgoing_buffers p) w)\<rparr>"


(* Okay, so my overall point is to refactor the code, and I'm working on that.
The other thing is working on the interpreter semantics. *)






end