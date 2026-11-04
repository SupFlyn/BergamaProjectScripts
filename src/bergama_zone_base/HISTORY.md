# bergama_zone_base: notes of older versions (moved out of the script header)

NEW IN v8 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_zone_base_log.txt (next to cached/ and output/), overwritten by each press.

NEW IN v7 (Aras 25 Oct 08:03-08:18): DEMETER'S GARDEN, Begum's idea alone (card i01), as zones DG 1 and DG 2 on
layer INT_ZONE_DG (tier D), where her drawing puts them: the south-west bank either side of K5 Uckemer bridge,
inside calisma_alan[1]. Outline = the open ground between the bed (WA 4 / WA 5) and the street edge less 1.5 m,
1.5 m clear of surveyed buildings and walls, 20 m clear of the K5 deck (DG 1 about 565 m2 upstream, DG 2 about
852 m2 downstream; placeholders, calculated from the survey DXF). Labels "DEMETER'S GARDEN" on each, and one very
small "idea: Begum" credit. Allowed as a public, educational garden with a cafe (Aras 08:07), so the 18 Oct "no
farmland inside the site" rule still holds for everything else. Everything else is as in v6.

NEW IN v6 (Aras 25 Oct 07:50-07:52: one file for everything, the larger survey "Bergama Müdahele Alanları (1)"): a
file with no study-area layers (aras_alan, begum_alan, nil_alan) is accepted when its survey (stream, buildings)
lies on the study areas recorded in STUDY_BBOX, i.e. it is the survey in survey coordinates; the base is baked
exactly as in v5. A file that HAS study-area layers must still have them where the course survey has them.
The working area is the whole calisma_alan, one shared area (Aras 25 Oct 08:05: no split by person). Every
proposal is baked whole when it lies in, crosses or comes within SNAP_M (15 m) of it (Aras 08:10-08:11: small
differences do not matter, lines that nearly match count as overlapping and the larger area is the true one); one
lying farther off is not baked and the log lists it. Labels are notes, baked as before.
calisma_alan is read from the open file (Bergama_Altlik.3dm; an open outline with ends under 5 m apart counts as
closed); with none there, the copy CALISMA_COPY below. The zones themselves are the same as in v5.
