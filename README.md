# Main Parser
- parser_13.py

# done

- [x] условие(сальдо>100, 0, 10)\
- [x] условие(сальдо>100, 0, 10) + условие(кредит<200, 5, 7)\
- [x] условие(сальдо>100, 0, условие(вклад>300, 11, 12)) + условие(кредит<200, 5, 7)
- [x] условие(сальдо+условие(вклад>300, 5, условие(выручка>123, 333, 444))>100, 2, 10) + условие(условие(долг<500, 13, 17)-кредит>200, 7, 9) - условие(штраф<300, 11, 12)

# todo

- [ ] условие(условие(сальдо>100, 0, 10) + условие(кредит<200, 5, 7) > 100, 0, 10)
- [ ] ..(условие() + условие() > условие(), ...)