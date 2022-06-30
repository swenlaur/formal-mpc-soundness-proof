theory CompleteExecution02
  imports 
    Main 
    AdversarialAction 
    BasicState
    ProtocolParty
    StandardFunctionality
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/data_types/DataTypes"
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/network_components/Functionality"
begin

(* ============= Näide: 2 mängijat, 2 funktsionaalsust, keskkond ========================== *)

  (* Mängija 1 *)
consts parameters1 :: "public_param * private_param"
consts code1 :: "cmd list"
definition interpreter1 :: stateful_interpreter where 
"interpreter1 =
  \<lparr>
  int_public_params = fst (parameters1),
  int_private_params = snd (parameters1),
  int_program = code1,
  int_incoming_buffers = [],
  int_outgoing_buffers = [],
  int_count_and_state = \<lambda>x. None,
  int_port_count = 2
  \<rparr>"
definition party1 :: protocol_party where 
"party1 = 
  \<lparr>
  party_interpreter = interpreter1,
  party_corrupted = False,
  party_incoming_buffers =  map_of [(0, []),(1, [])],
  party_outgoing_buffers =  map_of [(0, []),(1, [])]
  \<rparr>"

  (* Mängija 2 *)
consts parameters2 :: "public_param * private_param"
consts code2 :: "cmd list"
definition interpreter2 :: stateful_interpreter where 
"interpreter2 =
  \<lparr>
  int_public_params = fst (parameters2),
  int_private_params = snd (parameters2),
  int_program = code2,
  int_incoming_buffers = [],
  int_outgoing_buffers = [],
  int_count_and_state = \<lambda>x. None,
  int_port_count = 2
  \<rparr>"
definition party2 :: protocol_party where 
"party2 = 
  \<lparr>
  party_interpreter = interpreter2,
  party_corrupted = False,
  party_incoming_buffers =  map_of [(0, []),(1, [])],
  party_outgoing_buffers =  map_of [(0, []),(1, [])]
  \<rparr>"

  (* Funktsionaalsus 1 *)
definition fnl1 :: functionality where
"fnl1 = 
  \<lparr>
  fnl_outgoing_buffers = [[],[]], 
  fnl_is_env = False
  \<rparr>"

  (* Funktsionaalsus 2 *)
definition fnl2 :: functionality where
"fnl2 = 
  \<lparr>
  fnl_outgoing_buffers = [[],[]], 
  fnl_is_env = False
  \<rparr>"

  (* Funktsionaalsus 3: keskkond *)
definition env :: functionality where
"env = 
  \<lparr>
  fnl_outgoing_buffers = [[],[]], 
  fnl_is_env = True
  \<rparr>"


  (* Mängijate map *)
definition protocol_parties_00 where
"protocol_parties_00 = map_of [(1, party1), (2, party2)]"

  (* Funktsionaalsuste map *)
definition protocol_fnls_00  where
"protocol_fnls_00 = map_of [(1, fnl1), (2, fnl2), (3, env)]"

  (* Laziness checki signaalide map *)
     (* nimetada ümber? *)
definition outgoing_signals_00 where
"outgoing_signals_00 = (\<lambda>x. None)"

  (* Olek *)
definition system_state_00 where
"system_state_00 = 
  \<lparr>
  state_protocol_parties = protocol_parties_00,
  state_functionalities = protocol_fnls_00,
  state_corrupted_parties = {},
  state_outgoing_signals = outgoing_signals_00,
  state_previous_action = Empty,
  state_flag = True
  \<rparr>"

(* ============================================================================================== *)
(* Võiks olla abstraktne trustedsetup \<longrightarrow> system state *)

(* NB!

datatype adv_input =  
  AdvNone |             
  CorruptionReply "(instance_label, instance_state \<times> nat) map \<times> public_param \<times> private_param" |
  PeekReply msg |
  ClockIncomingReply "(nat \<times> msg) option" |
  SendIncomingReply write_instructions |
  QueryFunctionalityReply "msg * write_instructions"

*)

(* -------- helperid adv_clock_incoming_buffer & adv_clock_outgoing_buffer jaoks --------------- *) 

fun adv_clock_laziness_check :: "system_state \<Rightarrow> system_state" where
"adv_clock_laziness_check s = (if (\<exists>p func party'. 
          state_protocol_parties s p = Some party'
        \<and> is_corrupted party'
        \<and> \<not>(empty_incoming_buffer party' func)) 
           then s\<lparr>state_flag := False\<rparr>
           else s)"

fun adv_clock_flag_1 :: "system_state \<Rightarrow> bool" where
"adv_clock_flag_1 s = (if (\<exists>p func part.
          state_protocol_parties s p = Some part
        \<and> is_corrupted part
        \<and> \<not>(empty_incoming_buffer part func)) 
then False else True)"

fun adv_clock_flag_2 :: "system_state \<Rightarrow> buffer_action \<Rightarrow> msg \<Rightarrow> bool" where
"adv_clock_flag_2 s b m = 
(let (t1, t2) = get_protocol_instances m in
(case (state_outgoing_signals s) ((bufferParty b), (bufferFunc b), t1, t2) of
None \<Rightarrow> False |
Some boolean \<Rightarrow>  boolean))"

fun adv_clock_outgoing_buffer_1 :: "system_state \<Rightarrow> buffer_action \<Rightarrow> msg \<Rightarrow> system_state * adv_input"
  where
"adv_clock_outgoing_buffer_1 s b m =(let flag_1 = adv_clock_flag_1 s  in
(let new_func_map = map_upds (state_functionalities s) 
                             [bufferFunc b]
                             [fnl_update ((state_functionalities s) (bufferFunc b)) (bufferParty b) m]  in
(let new_signals = state_outgoing_signals s in 
(let flag_2 = adv_clock_flag_2 s b m in
(s\<lparr>state_flag := flag_1 \<and> flag_2,
   state_functionalities := new_func_map,
   state_outgoing_signals := new_signals\<rparr>, AdvNone)))))" 

(* ---------------------------------------------------------------------------------------------- *)


fun no_action :: "system_state \<Rightarrow> system_state * adv_input" where
(* 
Võtab:
süsteemi olek s 

Annab:
sama olek s, 
tühi vastus AdvNone 
*)
"no_action s = (s, AdvNone)"

fun adv_corrupt_party :: "system_state \<Rightarrow> party_id \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
(* 
Võtab:
s: süsteemi olek
p: korrumpeeritava mängija party_id
party: mängija

Annab:
s:
  1. corrupted_parties hulka on lisatud p
  2. protocol_parties loend on uuendatud nii, et p väärtus on nüüd korrumpeeritud party,
  3. eelmine tegevus on nüüd korrumpeerimine,
tühivastuse AdvNone 
*)
"adv_corrupt_party s p party =
  (s\<lparr>
    state_corrupted_parties := insert p (state_corrupted_parties s),
    state_protocol_parties := (state_protocol_parties s) (p := corrupt_party party),
    state_previous_action := CorruptParty p
    \<rparr>, AdvNone
  )"



fun adv_peek_incoming_buffer :: "system_state \<Rightarrow> buffer_action \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
(* 
s: olek
b: BufferAction record (vt AdversarialAction.thy)
party: mängija

\<Rightarrow> 
olek, mille PreviousAction on nüüd b,
vastus PeekReply m, (vastuse tüüp: AdvInput'i väli PeekReply msg)
*)
"adv_peek_incoming_buffer s b party =
(case peek_incoming_buffer party (bufferFunc b) (bufferInd b) of
None \<Rightarrow> no_action s |
Some m \<Rightarrow> (s\<lparr>state_previous_action := BufferAction b\<rparr>, PeekReply m))"



fun adv_peek_outgoing_buffer :: "system_state \<Rightarrow> buffer_action \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
(* 
s: olek
b: BufferAction record (vt AdversarialAction.thy)
party: mängija

\<Rightarrow> 
olek, mille PreviousAction on nüüd b,
vastus PeekReply m, (vastuse tüüp: AdvInput'i väli PeekReply msg)
*)
"adv_peek_outgoing_buffer s b party =
(case peek_outgoing_buffer party (bufferFunc b) (bufferInd b) of
None \<Rightarrow> no_action s|
Some m \<Rightarrow> (s\<lparr>state_previous_action := BufferAction b\<rparr>, PeekReply m))"

fun adv_clock_incoming_buffer :: "system_state \<Rightarrow> buffer_action \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
"adv_clock_incoming_buffer s b party = 
(let s0 = adv_clock_laziness_check s in
(let (opt_m, p) = (clock_message party (bufferFunc b) (bufferInd b)) in
(case opt_m of 
  None \<Rightarrow> no_action s |
  Some m \<Rightarrow>
    (let (write_instructions, reply) = party_make_write_instructions party (bufferFunc b) m in
    (case reply of
    None \<Rightarrow> 
    (s0\<lparr>
        state_protocol_parties := map_upds (state_protocol_parties s) [bufferParty b] [do_write_instructions party write_instructions],
        state_previous_action := BufferAction b
       \<rparr>,ClockIncomingReply reply) |
    Some r \<Rightarrow> 
    (s0\<lparr>
        state_previous_action := BufferAction b
       \<rparr>, ClockIncomingReply reply)
)))))"

(* and what the new signals are supposed to be. *)


fun adv_clock_outgoing_buffer :: "system_state \<Rightarrow> buffer_action \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
"adv_clock_outgoing_buffer s b party = 
(case (state_functionalities s) (bufferFunc b) of
None \<Rightarrow> no_action s |
Some func \<Rightarrow>
(let (opt_m, p) = (clock_message party (bufferFunc b) (bufferInd b)) in
(case opt_m of 
None \<Rightarrow> no_action s |
Some m \<Rightarrow> adv_clock_outgoing_buffer_1 s b m 
)))"
(* (Env võib sõnumit saades kirjutada igasse olemasolevasse porti) *)


fun adv_buffer_action :: "system_state \<Rightarrow> buffer_action \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
"adv_buffer_action s b party = 
(case bufferAction b of
Peek \<Rightarrow>
(case bufferDirection b of
Incoming \<Rightarrow> adv_peek_incoming_buffer s b party |
Outgoing \<Rightarrow> adv_peek_outgoing_buffer s b party )|
Clock \<Rightarrow> 
(case bufferDirection b of
Incoming \<Rightarrow> adv_clock_incoming_buffer s b party |
Outgoing \<Rightarrow> adv_clock_outgoing_buffer s b party))"


fun adv_send_message :: "system_state \<Rightarrow> send_message \<Rightarrow> protocol_party \<Rightarrow>  system_state * adv_input" where
"adv_send_message s send party =
(let m = sendMessage send in
(let (write_instructions, reply) = party_make_write_instructions party (sendFunc send) m in
(case reply of
None \<Rightarrow> 
  (s\<lparr>
    state_protocol_parties := map_upds (state_protocol_parties s) [sendParty send] [do_write_instructions party write_instructions],
    state_previous_action := SendMessage send
    \<rparr>, ClockIncomingReply reply) |
Some r \<Rightarrow> 
(s\<lparr>state_previous_action := SendMessage send\<rparr>, ClockIncomingReply reply))))"

(* 
fnl_adv_probe annab reply, write_instructions ja func_state.
pärast seda toimub nii:
evaluate(write_instructions) mängijates
update state w/ new func_state
*)
fun adv_query_functionality ::
"system_state \<Rightarrow> query_functionality \<Rightarrow> functionality \<Rightarrow> system_state * adv_input" where
"adv_query_functionality s q fnl = 
  (s, QueryFunctionalityReply (fnl_adv_probe fnl (queryMessage q)))"


(* Empty miks? *)
(* TODO: add Clock \<rightarrow> Send laziness test. *)
fun adv_step ::
"system_state  \<times> adv_action \<Rightarrow> system_state \<times> adv_input" where
"adv_step (s, action)  =
(case action of
Empty => no_action s |
CorruptParty p \<Rightarrow> 
  (case state_protocol_parties s p of
  None \<Rightarrow> no_action s |
  Some party \<Rightarrow> adv_corrupt_party s p party) |
BufferAction b \<Rightarrow>
  (case (state_protocol_parties s) (bufferParty b) of 
  None \<Rightarrow> no_action s |
  Some party \<Rightarrow> adv_buffer_action s b party) |
SendMessage send \<Rightarrow>
  (case (state_protocol_parties s) (sendParty send) of
  None \<Rightarrow> no_action s |
  Some party \<Rightarrow> adv_send_message s send party) |
QueryFunctionality q \<Rightarrow> 
  (case (state_functionalities s) (queryTarget q) of
  None \<Rightarrow>  no_action s |
  Some fnl \<Rightarrow> adv_query_functionality s q fnl))"


consts trusted_setup :: "system_state"
consts input_to_action :: "system_state * adv_input \<Rightarrow> system_state * adv_action"

fun exec :: "system_state *  adv_action \<Rightarrow> system_state * adv_action" where
"exec (s, a) = input_to_action (adv_step (trusted_setup, a))"


(* What is this?*)
definition full_exec :: bool where
"full_exec = True"

consts finalize :: "func_state \<Rightarrow> bool"





end
