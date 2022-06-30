theory ProtocolParty
  imports 
    Main 
    StatefulInterpreter
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/data_types/DataTypes"
begin

(* If k is the number of functionalities, then there are k+2 *)
record protocol_party =
  party_interpreter :: stateful_interpreter
  party_corrupted :: bool
  party_incoming_buffers :: "(functionality_id, msg list) map"
  party_outgoing_buffers :: "(functionality_id, msg list) map"

definition is_corrupted :: 
"'a protocol_party_scheme \<Rightarrow> bool" where
"is_corrupted p = party_corrupted p"

definition corrupt_party ::
"'a protocol_party_scheme \<Rightarrow> 'a protocol_party_scheme option" where
"corrupt_party p = Some (p\<lparr>party_corrupted := True\<rparr>)"

(* (instance_label, instance_state \<times> nat) map \<Rightarrow> interpreter_state *)
definition internal_state :: 
"'a protocol_party_scheme 
\<Rightarrow> (instance_label, nat * nat * instance_state) map \<times> public_param \<times> private_param" where
"internal_state p = reveal_state (party_interpreter p)"

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

definition update_outgoing_buffers :: (* [] \<Rightarrow>  msg list list *)
"(functionality_id, msg list) map \<Rightarrow> (functionality_id \<times> msg) list \<Rightarrow> (functionality_id, msg list) map" where
"update_outgoing_buffers bs ws = (map_upds bs (fst_unzip ws) [])"

(* peek ja pop message = clock message? *)
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

definition peek_incoming_buffer ::
"'a protocol_party_scheme \<Rightarrow> functionality_id \<Rightarrow> msg_index \<Rightarrow> msg option" where
"peek_incoming_buffer p f n = map_option
  (\<lambda>msglist. nth msglist n) (party_incoming_buffers p f)"

definition peek_outgoing_buffer ::
"'a protocol_party_scheme \<Rightarrow> functionality_id \<Rightarrow> msg_index \<Rightarrow> msg option" where
"peek_outgoing_buffer p f n = 
(case (party_outgoing_buffers p f) of 
None \<Rightarrow> None |
Some msglist \<Rightarrow> Some (nth msglist n))"

(* Party methods *)
definition do_write_instructions ::
"'a protocol_party_scheme \<Rightarrow> (functionality_id \<times> msg) list \<Rightarrow> 'a protocol_party_scheme" where
"do_write_instructions p w = p\<lparr>party_outgoing_buffers := (update_outgoing_buffers (party_outgoing_buffers p) w)\<rparr>"

definition party_make_write_instructions :: "'a protocol_party_scheme \<Rightarrow> functionality_id \<Rightarrow> msg  \<Rightarrow> write_instructions \<times> ((functionality_id \<times> msg) option)" where
"party_make_write_instructions p f m = (if party_corrupted p = True then ([], Some (f, m)) 
               else (interpreter_call (party_interpreter p), None))"

end