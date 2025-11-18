window.BENCHMARK_DATA = {
  "lastUpdate": 1763455082233,
  "repoUrl": "https://github.com/developmentseed/morecantile",
  "entries": {
    "morecantile Benchmarks": [
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bb213ea0544a0e6224056671e47bec7325a543bd",
          "message": "Merge pull request #160 from developmentseed/feature/add-benchmark\n\nadd benchmark",
          "timestamp": "2024-10-17T22:47:12+02:00",
          "tree_id": "7c1d86809f50b0a33e7f916acf39c7cc40bc57f9",
          "url": "https://github.com/developmentseed/morecantile/commit/bb213ea0544a0e6224056671e47bec7325a543bd"
        },
        "date": 1729198168968,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 27835.938458267672,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017434435174240333",
            "extra": "mean: 35.92478124993791 usec\nrounds: 5888"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 27190.417465309398,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029412499977205734",
            "extra": "mean: 36.77766261867216 usec\nrounds: 15069"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 27249.58197807611,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020329423375510278",
            "extra": "mean: 36.69781066016201 usec\nrounds: 15966"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 26643.22658150052,
            "unit": "iter/sec",
            "range": "stddev: 0.000001992104799157507",
            "extra": "mean: 37.53299161950381 usec\nrounds: 15751"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 26012.147536546607,
            "unit": "iter/sec",
            "range": "stddev: 0.000002246285965983132",
            "extra": "mean: 38.4435771246883 usec\nrounds: 15449"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 24755.893137511663,
            "unit": "iter/sec",
            "range": "stddev: 0.000002145666813328207",
            "extra": "mean: 40.394422226873246 usec\nrounds: 14883"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 7599.18515262934,
            "unit": "iter/sec",
            "range": "stddev: 0.000012997487183763481",
            "extra": "mean: 131.59305634946887 usec\nrounds: 3780"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 165628.37008686937,
            "unit": "iter/sec",
            "range": "stddev: 5.95158167760805e-7",
            "extra": "mean: 6.037612997552994 usec\nrounds: 76953"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 157629.40712018148,
            "unit": "iter/sec",
            "range": "stddev: 7.726803064542622e-7",
            "extra": "mean: 6.343993917566216 usec\nrounds: 77436"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 158075.76267245348,
            "unit": "iter/sec",
            "range": "stddev: 6.364320456934438e-7",
            "extra": "mean: 6.3260805014876675 usec\nrounds: 76185"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 133440.66227662732,
            "unit": "iter/sec",
            "range": "stddev: 6.199191767111791e-7",
            "extra": "mean: 7.493967602820825 usec\nrounds: 47504"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 124840.96934567855,
            "unit": "iter/sec",
            "range": "stddev: 6.510104949049002e-7",
            "extra": "mean: 8.010190927235184 usec\nrounds: 60489"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 103384.53478221432,
            "unit": "iter/sec",
            "range": "stddev: 7.226376914280621e-7",
            "extra": "mean: 9.672626588750044 usec\nrounds: 54128"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 10429.78059390976,
            "unit": "iter/sec",
            "range": "stddev: 0.00002334284555282665",
            "extra": "mean: 95.87929400776926 usec\nrounds: 5891"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "distinct": true,
          "id": "1dbb5fa5dd1a2a3e945879978c3e936f7f9d6344",
          "message": "add benchmark in docs",
          "timestamp": "2024-10-17T22:51:26+02:00",
          "tree_id": "955422a0c9695300ac609b5a6207acdf347d4586",
          "url": "https://github.com/developmentseed/morecantile/commit/1dbb5fa5dd1a2a3e945879978c3e936f7f9d6344"
        },
        "date": 1729198421361,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 27913.906746128847,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018496082253852282",
            "extra": "mean: 35.824437227464834 usec\nrounds: 7113"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 27256.043926344726,
            "unit": "iter/sec",
            "range": "stddev: 0.0000038042771849057276",
            "extra": "mean: 36.689110228261534 usec\nrounds: 15604"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 27351.332755728756,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019320418572744497",
            "extra": "mean: 36.56128967940508 usec\nrounds: 16249"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 26691.240814766465,
            "unit": "iter/sec",
            "range": "stddev: 0.000002347806963273008",
            "extra": "mean: 37.46547442061095 usec\nrounds: 15657"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 26198.032352728966,
            "unit": "iter/sec",
            "range": "stddev: 0.000002057823788672129",
            "extra": "mean: 38.170805598529356 usec\nrounds: 15468"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 25012.554568666845,
            "unit": "iter/sec",
            "range": "stddev: 0.00000422723314710326",
            "extra": "mean: 39.97992277257026 usec\nrounds: 15163"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 7681.622103516133,
            "unit": "iter/sec",
            "range": "stddev: 0.000005903618807971685",
            "extra": "mean: 130.1808376569666 usec\nrounds: 3739"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 160102.465576479,
            "unit": "iter/sec",
            "range": "stddev: 5.217579070424924e-7",
            "extra": "mean: 6.246000000058164 usec\nrounds: 75104"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 155636.15792707624,
            "unit": "iter/sec",
            "range": "stddev: 5.17274984630616e-7",
            "extra": "mean: 6.4252421372966095 usec\nrounds: 74879"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 157382.49612296972,
            "unit": "iter/sec",
            "range": "stddev: 5.86760529741576e-7",
            "extra": "mean: 6.35394675160481 usec\nrounds: 78162"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 135321.18951175586,
            "unit": "iter/sec",
            "range": "stddev: 6.039978442942694e-7",
            "extra": "mean: 7.38982567037756 usec\nrounds: 64814"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 125607.01929312383,
            "unit": "iter/sec",
            "range": "stddev: 6.494169678927579e-7",
            "extra": "mean: 7.961338511395944 usec\nrounds: 64438"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 103897.79050448934,
            "unit": "iter/sec",
            "range": "stddev: 6.9194280633227e-7",
            "extra": "mean: 9.624843754081477 usec\nrounds: 54043"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 10863.451936572368,
            "unit": "iter/sec",
            "range": "stddev: 0.000004862943424056361",
            "extra": "mean: 92.0517719265134 usec\nrounds: 5906"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "b2704d20d53c23fac68a4354b5ca60040642669f",
          "message": "Merge pull request #161 from developmentseed/feature/performance-improvement\n\nPerformance improvement",
          "timestamp": "2024-10-17T23:04:15+02:00",
          "tree_id": "202b38ce0e9e3682db11118d28f19bf367c75cc1",
          "url": "https://github.com/developmentseed/morecantile/commit/b2704d20d53c23fac68a4354b5ca60040642669f"
        },
        "date": 1729199199320,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 24862.11453559257,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019492129950717947",
            "extra": "mean: 40.22184028508119 usec\nrounds: 5754"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 24852.18553495046,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030728462641287322",
            "extra": "mean: 40.23790980449854 usec\nrounds: 14779"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 23683.697060960614,
            "unit": "iter/sec",
            "range": "stddev: 0.000007904259426535646",
            "extra": "mean: 42.223137604996865 usec\nrounds: 15014"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 24990.58764421827,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018203211163701935",
            "extra": "mean: 40.015065441302504 usec\nrounds: 15235"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 24725.800513145387,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017323404691663823",
            "extra": "mean: 40.44358440360114 usec\nrounds: 15260"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 24728.720114726373,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015778154743725443",
            "extra": "mean: 40.438809423237515 usec\nrounds: 15133"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 11510.54950673721,
            "unit": "iter/sec",
            "range": "stddev: 0.0000046125642341575415",
            "extra": "mean: 86.87682542129657 usec\nrounds: 3918"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 247568.9310958904,
            "unit": "iter/sec",
            "range": "stddev: 4.2001181176820506e-7",
            "extra": "mean: 4.039279062899342 usec\nrounds: 76782"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 245528.44881440885,
            "unit": "iter/sec",
            "range": "stddev: 4.048445354124478e-7",
            "extra": "mean: 4.072847789446528 usec\nrounds: 81880"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 245698.17672196857,
            "unit": "iter/sec",
            "range": "stddev: 4.630466337046226e-7",
            "extra": "mean: 4.070034272706864 usec\nrounds: 63695"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 247604.02477760866,
            "unit": "iter/sec",
            "range": "stddev: 4.464137351145614e-7",
            "extra": "mean: 4.038706563425912 usec\nrounds: 83599"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 242333.5174500791,
            "unit": "iter/sec",
            "range": "stddev: 4.568578119479004e-7",
            "extra": "mean: 4.126544320085647 usec\nrounds: 79975"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 241996.71427192705,
            "unit": "iter/sec",
            "range": "stddev: 4.3860826458705846e-7",
            "extra": "mean: 4.132287510632558 usec\nrounds: 78971"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 21826.21730472572,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028660382744233347",
            "extra": "mean: 45.81645944592901 usec\nrounds: 7977"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "distinct": true,
          "id": "0ab27a724b762764eaa4c320b2cdf219a7d1d06c",
          "message": "Bump version: 6.0.0 → 6.1.0",
          "timestamp": "2024-10-17T23:06:40+02:00",
          "tree_id": "c92056687c95762a4516acbd3210b0674eedea8f",
          "url": "https://github.com/developmentseed/morecantile/commit/0ab27a724b762764eaa4c320b2cdf219a7d1d06c"
        },
        "date": 1729199426105,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 25177.4766024677,
            "unit": "iter/sec",
            "range": "stddev: 0.000002180143224294346",
            "extra": "mean: 39.71803909459249 usec\nrounds: 5832"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 24909.039615157715,
            "unit": "iter/sec",
            "range": "stddev: 0.000002912934217095221",
            "extra": "mean: 40.146068072069596 usec\nrounds: 14705"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 24832.059746489256,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019837911485453677",
            "extra": "mean: 40.27052166469515 usec\nrounds: 15186"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 24965.319148442453,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025655964249881395",
            "extra": "mean: 40.055566446158906 usec\nrounds: 15569"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 25033.888606880362,
            "unit": "iter/sec",
            "range": "stddev: 0.000002427593286639022",
            "extra": "mean: 39.94585162950506 usec\nrounds: 15158"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 24994.230091614147,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025336538926136877",
            "extra": "mean: 40.00923398458717 usec\nrounds: 15048"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 11321.239330330172,
            "unit": "iter/sec",
            "range": "stddev: 0.000004581923359013787",
            "extra": "mean: 88.32955216492503 usec\nrounds: 4850"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 247186.63766424358,
            "unit": "iter/sec",
            "range": "stddev: 8.134244687509826e-7",
            "extra": "mean: 4.045526123294381 usec\nrounds: 81747"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 254914.79950257778,
            "unit": "iter/sec",
            "range": "stddev: 4.392793126949101e-7",
            "extra": "mean: 3.922879338317459 usec\nrounds: 78285"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 255989.10267732543,
            "unit": "iter/sec",
            "range": "stddev: 5.494969328733005e-7",
            "extra": "mean: 3.9064162870264885 usec\nrounds: 85823"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 255721.76836715138,
            "unit": "iter/sec",
            "range": "stddev: 4.2452091880239753e-7",
            "extra": "mean: 3.9105000969813974 usec\nrounds: 82488"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 248528.84474587048,
            "unit": "iter/sec",
            "range": "stddev: 5.657463432764732e-7",
            "extra": "mean: 4.023677819057725 usec\nrounds: 78040"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 248090.9011786786,
            "unit": "iter/sec",
            "range": "stddev: 4.663184717402086e-7",
            "extra": "mean: 4.030780634231264 usec\nrounds: 77797"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 21665.830359816795,
            "unit": "iter/sec",
            "range": "stddev: 0.000002875210373114192",
            "extra": "mean: 46.155627704658905 usec\nrounds: 8735"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "665a9842050fd625d0dec552aa70f2482f318a74",
          "message": "Merge pull request #171 from developmentseed/feature/python-version-support\n\nupdate python version support and update pyproj version requirement",
          "timestamp": "2024-12-19T16:31:55+01:00",
          "tree_id": "b545af35bd2ef0a8c2e7813d1fb45dcda8c261ac",
          "url": "https://github.com/developmentseed/morecantile/commit/665a9842050fd625d0dec552aa70f2482f318a74"
        },
        "date": 1734622440489,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 26220.10895897432,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020727354842466196",
            "extra": "mean: 38.138666836383656 usec\nrounds: 5928"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 26143.694409322477,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021703630663501093",
            "extra": "mean: 38.25014109878113 usec\nrounds: 14536"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 26138.588184917924,
            "unit": "iter/sec",
            "range": "stddev: 0.000002156622890016091",
            "extra": "mean: 38.25761333877261 usec\nrounds: 14889"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 26272.52106950504,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024008849999524132",
            "extra": "mean: 38.062582473697844 usec\nrounds: 14744"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 26236.67764877277,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024207587609113584",
            "extra": "mean: 38.1145819370455 usec\nrounds: 15225"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 26071.526128599675,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022704143299747398",
            "extra": "mean: 38.356020858442584 usec\nrounds: 14958"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 12493.083254914018,
            "unit": "iter/sec",
            "range": "stddev: 0.000004963038064592171",
            "extra": "mean: 80.04429167688937 usec\nrounds: 3713"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 263848.1632580246,
            "unit": "iter/sec",
            "range": "stddev: 4.7298228849773226e-7",
            "extra": "mean: 3.7900585990514233 usec\nrounds: 72015"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 245692.8554099457,
            "unit": "iter/sec",
            "range": "stddev: 0.000001813687869291026",
            "extra": "mean: 4.070122423102091 usec\nrounds: 71449"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 264800.60154661455,
            "unit": "iter/sec",
            "range": "stddev: 4.212396103117613e-7",
            "extra": "mean: 3.776426466402734 usec\nrounds: 70097"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 263266.7470293282,
            "unit": "iter/sec",
            "range": "stddev: 3.9171500934372525e-7",
            "extra": "mean: 3.7984288227962146 usec\nrounds: 43722"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 257851.72018831366,
            "unit": "iter/sec",
            "range": "stddev: 4.560416713192813e-7",
            "extra": "mean: 3.878197900986204 usec\nrounds: 52122"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 256060.00757253324,
            "unit": "iter/sec",
            "range": "stddev: 4.461552434715241e-7",
            "extra": "mean: 3.905334571689151 usec\nrounds: 71342"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24521.159640311103,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033476940812014017",
            "extra": "mean: 40.78110557039352 usec\nrounds: 9103"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "distinct": true,
          "id": "93f8041aaf894c74ca8f21bb56972d88f16111b7",
          "message": "Bump version: 6.1.0 → 6.2.0",
          "timestamp": "2024-12-19T16:33:43+01:00",
          "tree_id": "4e0ddf7e3a9151a7ebc7de6f5899d6e3ed2ad06e",
          "url": "https://github.com/developmentseed/morecantile/commit/93f8041aaf894c74ca8f21bb56972d88f16111b7"
        },
        "date": 1734622558430,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 26650.46810759589,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025412834930625765",
            "extra": "mean: 37.52279306925122 usec\nrounds: 6089"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 26320.34779257724,
            "unit": "iter/sec",
            "range": "stddev: 0.00000386489185346555",
            "extra": "mean: 37.99341892746631 usec\nrounds: 14561"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 26282.96110142204,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024042146887196868",
            "extra": "mean: 38.047463379074706 usec\nrounds: 15128"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 26024.427466192687,
            "unit": "iter/sec",
            "range": "stddev: 0.0000043654541995237615",
            "extra": "mean: 38.42543707442021 usec\nrounds: 15121"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 26260.65183128418,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031282787784744554",
            "extra": "mean: 38.07978592552319 usec\nrounds: 14878"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 26256.491759969467,
            "unit": "iter/sec",
            "range": "stddev: 0.000002141148475174607",
            "extra": "mean: 38.08581927630544 usec\nrounds: 15117"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 12497.1290823193,
            "unit": "iter/sec",
            "range": "stddev: 0.000004023491716503878",
            "extra": "mean: 80.01837809411612 usec\nrounds: 4766"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 264018.8170856358,
            "unit": "iter/sec",
            "range": "stddev: 4.3729564212100437e-7",
            "extra": "mean: 3.787608819092789 usec\nrounds: 77197"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 260724.36720634482,
            "unit": "iter/sec",
            "range": "stddev: 4.4706290212366355e-7",
            "extra": "mean: 3.8354681256492262 usec\nrounds: 75672"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 262564.49389817496,
            "unit": "iter/sec",
            "range": "stddev: 3.9682955262713536e-7",
            "extra": "mean: 3.808588073556547 usec\nrounds: 82556"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 248814.30306578334,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037593045027518957",
            "extra": "mean: 4.019061555860849 usec\nrounds: 80496"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 255098.60183701068,
            "unit": "iter/sec",
            "range": "stddev: 4.735753060784604e-7",
            "extra": "mean: 3.920052845444158 usec\nrounds: 75787"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 251930.9678017437,
            "unit": "iter/sec",
            "range": "stddev: 4.389737350191762e-7",
            "extra": "mean: 3.9693413188764746 usec\nrounds: 76430"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24349.106969361164,
            "unit": "iter/sec",
            "range": "stddev: 0.000003230845595461544",
            "extra": "mean: 41.06926801292198 usec\nrounds: 8466"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c317ec76618875f467594b70f7473da2f1aa4ab8",
          "message": "Merge pull request #172 from developmentseed/feature/remove-python3.8\n\nremove python 3.8",
          "timestamp": "2024-12-19T16:40:25+01:00",
          "tree_id": "d0778d96ecef13a6ae15c39a122cb89689f168bb",
          "url": "https://github.com/developmentseed/morecantile/commit/c317ec76618875f467594b70f7473da2f1aa4ab8"
        },
        "date": 1734622955685,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 26425.154867344227,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018313770670244654",
            "extra": "mean: 37.842729967716615 usec\nrounds: 5903"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 25775.14184495227,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018059012703344244",
            "extra": "mean: 38.79707068210905 usec\nrounds: 14162"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 25337.141539314674,
            "unit": "iter/sec",
            "range": "stddev: 0.000007284334294175872",
            "extra": "mean: 39.46775126343034 usec\nrounds: 14843"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 24666.33916351012,
            "unit": "iter/sec",
            "range": "stddev: 0.000011314657887225217",
            "extra": "mean: 40.54107881072758 usec\nrounds: 15239"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 25988.64283348443,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023994761355574023",
            "extra": "mean: 38.478346345641974 usec\nrounds: 14653"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 26098.43325105805,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018235251504639002",
            "extra": "mean: 38.316476333285614 usec\nrounds: 15021"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 12471.853280124173,
            "unit": "iter/sec",
            "range": "stddev: 0.000011139481919869445",
            "extra": "mean: 80.18054554840336 usec\nrounds: 4841"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 263453.2018209442,
            "unit": "iter/sec",
            "range": "stddev: 6.335971670042238e-7",
            "extra": "mean: 3.7957405455244735 usec\nrounds: 74884"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 263138.8227977063,
            "unit": "iter/sec",
            "range": "stddev: 4.862403361735983e-7",
            "extra": "mean: 3.8002754187616468 usec\nrounds: 70892"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 262646.6964212119,
            "unit": "iter/sec",
            "range": "stddev: 3.68749625060207e-7",
            "extra": "mean: 3.8073960709419303 usec\nrounds: 74267"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 264236.5936223653,
            "unit": "iter/sec",
            "range": "stddev: 4.285398370832908e-7",
            "extra": "mean: 3.7844871760235965 usec\nrounds: 72754"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 257365.23412915226,
            "unit": "iter/sec",
            "range": "stddev: 4.5220127391680337e-7",
            "extra": "mean: 3.885528686046909 usec\nrounds: 72701"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 256012.4765996892,
            "unit": "iter/sec",
            "range": "stddev: 4.389948404093841e-7",
            "extra": "mean: 3.9060596314750624 usec\nrounds: 73015"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24495.272352266053,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034009878749556094",
            "extra": "mean: 40.8242041818935 usec\nrounds: 9134"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "distinct": true,
          "id": "c36470615a5de83667a90c6c31720641062c31f2",
          "message": "really drop python 3.8",
          "timestamp": "2024-12-19T20:23:50+01:00",
          "tree_id": "951832b24daa0281060d6630c8caaec8583befc0",
          "url": "https://github.com/developmentseed/morecantile/commit/c36470615a5de83667a90c6c31720641062c31f2"
        },
        "date": 1734636360559,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 26372.729252489436,
            "unit": "iter/sec",
            "range": "stddev: 0.000002235484969571474",
            "extra": "mean: 37.91795647792523 usec\nrounds: 5974"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 26278.83228600919,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028089851077626308",
            "extra": "mean: 38.05344123043087 usec\nrounds: 14106"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 26055.075084815286,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023239518095135824",
            "extra": "mean: 38.38023865771905 usec\nrounds: 14724"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 26215.717933689466,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023566194165896223",
            "extra": "mean: 38.14505490673263 usec\nrounds: 14898"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 26245.69216478106,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023858201764736918",
            "extra": "mean: 38.10149085501712 usec\nrounds: 14489"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 26137.265800120957,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025013647610060943",
            "extra": "mean: 38.259548938564656 usec\nrounds: 14692"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 12376.472036601439,
            "unit": "iter/sec",
            "range": "stddev: 0.000005121453070440648",
            "extra": "mean: 80.79846963194841 usec\nrounds: 4676"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 263461.07319253084,
            "unit": "iter/sec",
            "range": "stddev: 4.290672187974146e-7",
            "extra": "mean: 3.79562714097511 usec\nrounds: 76600"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 259731.83661162484,
            "unit": "iter/sec",
            "range": "stddev: 4.2610478679918774e-7",
            "extra": "mean: 3.8501248558731476 usec\nrounds: 72908"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 260668.7366971283,
            "unit": "iter/sec",
            "range": "stddev: 4.080081665786388e-7",
            "extra": "mean: 3.8362866704721195 usec\nrounds: 75735"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 262334.7813347802,
            "unit": "iter/sec",
            "range": "stddev: 4.561728225687881e-7",
            "extra": "mean: 3.8119230508128603 usec\nrounds: 70592"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 253407.23940186817,
            "unit": "iter/sec",
            "range": "stddev: 4.5483370916526747e-7",
            "extra": "mean: 3.9462171734333955 usec\nrounds: 68885"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 255584.66373392552,
            "unit": "iter/sec",
            "range": "stddev: 4.414220063075638e-7",
            "extra": "mean: 3.9125978272352144 usec\nrounds: 69219"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24671.96584243602,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024272143873749082",
            "extra": "mean: 40.531833028075546 usec\nrounds: 8738"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "distinct": true,
          "id": "960096873af8a71735614dd97cc1d4c5268b5e12",
          "message": "update mkdocs deploy",
          "timestamp": "2024-12-19T20:35:13+01:00",
          "tree_id": "bde42be2923870585ef22afa5d2774f4ad59da5b",
          "url": "https://github.com/developmentseed/morecantile/commit/960096873af8a71735614dd97cc1d4c5268b5e12"
        },
        "date": 1734637042898,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 26016.98091251926,
            "unit": "iter/sec",
            "range": "stddev: 0.000004793175379005561",
            "extra": "mean: 38.43643516372818 usec\nrounds: 5938"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 26048.43153541352,
            "unit": "iter/sec",
            "range": "stddev: 0.000002522860172821024",
            "extra": "mean: 38.39002738573622 usec\nrounds: 14679"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 26035.951415682342,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022573059846682955",
            "extra": "mean: 38.40842933043983 usec\nrounds: 15056"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 26173.385325988453,
            "unit": "iter/sec",
            "range": "stddev: 0.000002281427619317998",
            "extra": "mean: 38.206750389567134 usec\nrounds: 14755"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 26014.238063382403,
            "unit": "iter/sec",
            "range": "stddev: 0.000002241663345450082",
            "extra": "mean: 38.440487765336414 usec\nrounds: 14181"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 25963.968660458788,
            "unit": "iter/sec",
            "range": "stddev: 0.0000021426201976779617",
            "extra": "mean: 38.514913227534684 usec\nrounds: 14636"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 12447.206578525434,
            "unit": "iter/sec",
            "range": "stddev: 0.000004110379085798354",
            "extra": "mean: 80.33931096839444 usec\nrounds: 4814"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 258103.21702905174,
            "unit": "iter/sec",
            "range": "stddev: 4.7600280611213476e-7",
            "extra": "mean: 3.874418968933043 usec\nrounds: 77316"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 259744.62233192235,
            "unit": "iter/sec",
            "range": "stddev: 3.779551062447088e-7",
            "extra": "mean: 3.849935336571167 usec\nrounds: 80045"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 258270.91415906476,
            "unit": "iter/sec",
            "range": "stddev: 4.032767928580372e-7",
            "extra": "mean: 3.8719032813122607 usec\nrounds: 80367"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 259718.9299046267,
            "unit": "iter/sec",
            "range": "stddev: 4.3944250537700516e-7",
            "extra": "mean: 3.8503161874539424 usec\nrounds: 70493"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 251655.82441203395,
            "unit": "iter/sec",
            "range": "stddev: 4.262056088857792e-7",
            "extra": "mean: 3.9736811271361976 usec\nrounds: 71552"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 248893.51764022346,
            "unit": "iter/sec",
            "range": "stddev: 4.5594753708194924e-7",
            "extra": "mean: 4.017782421499237 usec\nrounds: 70393"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24582.422534116664,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037002987579772583",
            "extra": "mean: 40.679473254198285 usec\nrounds: 8936"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "d9d3633e59966137c4ea4306be157f56f4a876dd",
          "message": "Merge pull request #177 from developmentseed/feature/strict_tile_validation\n\ncheck maxzoom in is_valid",
          "timestamp": "2025-09-04T09:30:26+02:00",
          "tree_id": "0816e4d0da4ba9ea0d779382c383c319bc3f083e",
          "url": "https://github.com/developmentseed/morecantile/commit/d9d3633e59966137c4ea4306be157f56f4a876dd"
        },
        "date": 1756971110433,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 24382.402061756522,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032514293056204476",
            "extra": "mean: 41.01318637381043 usec\nrounds: 7104"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 24175.56024143941,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029174885400768856",
            "extra": "mean: 41.36408794721111 usec\nrounds: 15009"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 24250.18119881419,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033200347548741503",
            "extra": "mean: 41.23680527586734 usec\nrounds: 15694"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 24411.97335398198,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029429739841211195",
            "extra": "mean: 40.96350530535394 usec\nrounds: 15456"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 24447.510997794292,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027532379861349265",
            "extra": "mean: 40.90395951106115 usec\nrounds: 15708"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 24284.774803585482,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028275046724315625",
            "extra": "mean: 41.17806354343285 usec\nrounds: 15753"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 12027.095916046857,
            "unit": "iter/sec",
            "range": "stddev: 0.00000873947189470495",
            "extra": "mean: 83.14559117016557 usec\nrounds: 5572"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 246420.54348221386,
            "unit": "iter/sec",
            "range": "stddev: 6.53841644169608e-7",
            "extra": "mean: 4.05810321602581 usec\nrounds: 59981"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 249023.68735937658,
            "unit": "iter/sec",
            "range": "stddev: 6.665337108179097e-7",
            "extra": "mean: 4.015682245347438 usec\nrounds: 83105"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 251000.70538017715,
            "unit": "iter/sec",
            "range": "stddev: 7.023169623280135e-7",
            "extra": "mean: 3.9840525487183567 usec\nrounds: 85749"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 249295.7319201029,
            "unit": "iter/sec",
            "range": "stddev: 8.027729816215016e-7",
            "extra": "mean: 4.011300122540771 usec\nrounds: 87321"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 243113.09072808776,
            "unit": "iter/sec",
            "range": "stddev: 7.103959952156245e-7",
            "extra": "mean: 4.113312026946587 usec\nrounds: 76894"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 243617.38663433076,
            "unit": "iter/sec",
            "range": "stddev: 8.27596397052143e-7",
            "extra": "mean: 4.1047973373961115 usec\nrounds: 79847"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24123.44696134577,
            "unit": "iter/sec",
            "range": "stddev: 0.000006937099609454965",
            "extra": "mean: 41.45344575351736 usec\nrounds: 9761"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "383c2b3ab43dca37a710fd6eb55369c451dc533a",
          "message": "Merge pull request #165 from developmentseed/patch/force-wgs84-for-geojson-feature\n\nuse WGS84 as default CRS for GeoJSON outputs",
          "timestamp": "2025-09-04T13:33:50+02:00",
          "tree_id": "985ebb5f8ea0f3b1c46b00e14ec6b0830e4c3da2",
          "url": "https://github.com/developmentseed/morecantile/commit/383c2b3ab43dca37a710fd6eb55369c451dc533a"
        },
        "date": 1756985720480,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 25491.11675034521,
            "unit": "iter/sec",
            "range": "stddev: 0.000002911922212026472",
            "extra": "mean: 39.229352318840945 usec\nrounds: 5671"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 25202.65359934056,
            "unit": "iter/sec",
            "range": "stddev: 0.000004116327140674216",
            "extra": "mean: 39.67836148913167 usec\nrounds: 13082"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 25024.02436858157,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026905081335377466",
            "extra": "mean: 39.96159791370451 usec\nrounds: 13900"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 24876.909734670982,
            "unit": "iter/sec",
            "range": "stddev: 0.000004312753972454989",
            "extra": "mean: 40.197918900123625 usec\nrounds: 14402"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 25212.819263346115,
            "unit": "iter/sec",
            "range": "stddev: 0.000002942395321870082",
            "extra": "mean: 39.6623634015328 usec\nrounds: 14323"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 24866.136804870537,
            "unit": "iter/sec",
            "range": "stddev: 0.000002711703218210727",
            "extra": "mean: 40.215334124765604 usec\nrounds: 14740"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 12229.987625965261,
            "unit": "iter/sec",
            "range": "stddev: 0.000006010129144177394",
            "extra": "mean: 81.76623154359686 usec\nrounds: 5066"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 248215.70095271492,
            "unit": "iter/sec",
            "range": "stddev: 6.199206614242301e-7",
            "extra": "mean: 4.028754007751105 usec\nrounds: 68555"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 247284.46725433436,
            "unit": "iter/sec",
            "range": "stddev: 6.375511432284074e-7",
            "extra": "mean: 4.043925650095486 usec\nrounds: 72643"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 247525.11304114058,
            "unit": "iter/sec",
            "range": "stddev: 7.001426400622333e-7",
            "extra": "mean: 4.039994114996293 usec\nrounds: 77316"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 248700.08453618424,
            "unit": "iter/sec",
            "range": "stddev: 6.135393428941742e-7",
            "extra": "mean: 4.020907358616142 usec\nrounds: 68274"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 243124.8653552165,
            "unit": "iter/sec",
            "range": "stddev: 6.783919663669527e-7",
            "extra": "mean: 4.113112817724153 usec\nrounds: 73180"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 243128.11395880757,
            "unit": "iter/sec",
            "range": "stddev: 7.904957736986943e-7",
            "extra": "mean: 4.113057859567104 usec\nrounds: 77256"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24388.273933357083,
            "unit": "iter/sec",
            "range": "stddev: 0.000003126989926398064",
            "extra": "mean: 41.003311785515464 usec\nrounds: 7874"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "74e8f4cbc77194a04e70384aeae2f72fff15bc76",
          "message": "Merge pull request #178 from developmentseed/feature/add-geographic-crs-options-in-tiles/tile\n\nadd geographic_crs option in tile and tiles methods",
          "timestamp": "2025-09-05T11:04:19+02:00",
          "tree_id": "0dedffe4a86fa055482baee66007cdd13884dd57",
          "url": "https://github.com/developmentseed/morecantile/commit/74e8f4cbc77194a04e70384aeae2f72fff15bc76"
        },
        "date": 1757063146838,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 55184.51728211597,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017866247041205095",
            "extra": "mean: 18.12102468682963 usec\nrounds: 10451"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 54897.43575243945,
            "unit": "iter/sec",
            "range": "stddev: 0.00000162139324245196",
            "extra": "mean: 18.215787063525337 usec\nrounds: 25200"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 54626.380102574316,
            "unit": "iter/sec",
            "range": "stddev: 0.000001543962504128386",
            "extra": "mean: 18.306173649475888 usec\nrounds: 27043"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 54926.57573924913,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014969204577643289",
            "extra": "mean: 18.20612311146543 usec\nrounds: 27138"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 54881.54905824729,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020682711813128784",
            "extra": "mean: 18.221060031280686 usec\nrounds: 26253"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 54315.72438784034,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020477209198377855",
            "extra": "mean: 18.410874774669672 usec\nrounds: 26632"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 17422.26536605876,
            "unit": "iter/sec",
            "range": "stddev: 0.000004221250774499297",
            "extra": "mean: 57.39781704554638 usec\nrounds: 6160"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 249601.66896451128,
            "unit": "iter/sec",
            "range": "stddev: 6.027586299238799e-7",
            "extra": "mean: 4.006383467500698 usec\nrounds: 79347"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 249801.0956668934,
            "unit": "iter/sec",
            "range": "stddev: 7.100710578769126e-7",
            "extra": "mean: 4.003185003373593 usec\nrounds: 86193"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 252823.94746815984,
            "unit": "iter/sec",
            "range": "stddev: 6.387692907280238e-7",
            "extra": "mean: 3.9553215192399374 usec\nrounds: 86648"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 253341.2066689102,
            "unit": "iter/sec",
            "range": "stddev: 5.853773186486754e-7",
            "extra": "mean: 3.9472457447749223 usec\nrounds: 82488"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 244773.23601942987,
            "unit": "iter/sec",
            "range": "stddev: 6.335892001571436e-7",
            "extra": "mean: 4.0854139785144685 usec\nrounds: 58032"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 245527.10398811224,
            "unit": "iter/sec",
            "range": "stddev: 7.221583079826098e-7",
            "extra": "mean: 4.0728700976671695 usec\nrounds: 79221"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24529.519513698022,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028596410360299904",
            "extra": "mean: 40.76720701526868 usec\nrounds: 10748"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c8d88eaae7e245a0f7a84ede4856dcaf9e514c38",
          "message": "Merge pull request #181 from developmentseed/feature/update-python-req\n\nremove python 3.9 and 3.10 support",
          "timestamp": "2025-09-05T11:41:56+02:00",
          "tree_id": "56c0692edb1eb64bf965f81247d0c95d644742f7",
          "url": "https://github.com/developmentseed/morecantile/commit/c8d88eaae7e245a0f7a84ede4856dcaf9e514c38"
        },
        "date": 1757065401774,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 55421.936190311346,
            "unit": "iter/sec",
            "range": "stddev: 0.000001692848271541141",
            "extra": "mean: 18.043397050693734 usec\nrounds: 7256"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 54838.664392575025,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019918138840008103",
            "extra": "mean: 18.235309176045448 usec\nrounds: 23485"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 53873.63836859946,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029872361262172334",
            "extra": "mean: 18.561954051777118 usec\nrounds: 24767"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 55477.63403209558,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017843517140187048",
            "extra": "mean: 18.02528203386374 usec\nrounds: 24997"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 54943.31813957101,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015157159750114008",
            "extra": "mean: 18.200575317634208 usec\nrounds: 23142"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 54679.36038526122,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016741714275549726",
            "extra": "mean: 18.2884363122424 usec\nrounds: 25468"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 17468.006216304555,
            "unit": "iter/sec",
            "range": "stddev: 0.000004267327327722398",
            "extra": "mean: 57.24751798328332 usec\nrounds: 6089"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 252914.54534525203,
            "unit": "iter/sec",
            "range": "stddev: 6.072634992829081e-7",
            "extra": "mean: 3.9539046622838803 usec\nrounds: 71210"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 252999.79517206535,
            "unit": "iter/sec",
            "range": "stddev: 6.014481082077006e-7",
            "extra": "mean: 3.952572369949546 usec\nrounds: 73449"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 253584.01610793857,
            "unit": "iter/sec",
            "range": "stddev: 5.736263974389827e-7",
            "extra": "mean: 3.9434662142678105 usec\nrounds: 83112"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 255293.5879201386,
            "unit": "iter/sec",
            "range": "stddev: 5.735213606114353e-7",
            "extra": "mean: 3.9170588190128055 usec\nrounds: 78223"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 246163.24397999336,
            "unit": "iter/sec",
            "range": "stddev: 6.716878604310587e-7",
            "extra": "mean: 4.06234490507963 usec\nrounds: 80109"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 247130.36487162497,
            "unit": "iter/sec",
            "range": "stddev: 7.10508760914414e-7",
            "extra": "mean: 4.046447309376421 usec\nrounds: 73068"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24513.74403127943,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028950491614823172",
            "extra": "mean: 40.793442189981434 usec\nrounds: 9315"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "988f02f08351aef68dd60bf2408c8cd07535fdb6",
          "message": "Merge pull request #183 from developmentseed/feature/overwrite-geographic-crs\n\nrefactor geographic crs attribute",
          "timestamp": "2025-09-18T13:28:47+02:00",
          "tree_id": "735bd141dc7c46884b5e8c84828d2fc5ab2b29e3",
          "url": "https://github.com/developmentseed/morecantile/commit/988f02f08351aef68dd60bf2408c8cd07535fdb6"
        },
        "date": 1758195013742,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 10791.46840195257,
            "unit": "iter/sec",
            "range": "stddev: 0.000011913137700706926",
            "extra": "mean: 92.66579512191905 usec\nrounds: 1025"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 10902.281491409452,
            "unit": "iter/sec",
            "range": "stddev: 0.0000067434129429147586",
            "extra": "mean: 91.72392042784426 usec\nrounds: 6736"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 10898.875472971691,
            "unit": "iter/sec",
            "range": "stddev: 0.00000862636893835814",
            "extra": "mean: 91.7525851616451 usec\nrounds: 6834"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 10930.498070025378,
            "unit": "iter/sec",
            "range": "stddev: 0.00000933043093011194",
            "extra": "mean: 91.48713934109666 usec\nrounds: 6947"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 11007.433046180216,
            "unit": "iter/sec",
            "range": "stddev: 0.000006335582684078878",
            "extra": "mean: 90.84770225761388 usec\nrounds: 7043"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 11027.987574987601,
            "unit": "iter/sec",
            "range": "stddev: 0.000007215321977746424",
            "extra": "mean: 90.67837565106473 usec\nrounds: 7105"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 6808.8368755845295,
            "unit": "iter/sec",
            "range": "stddev: 0.000010025074449657718",
            "extra": "mean: 146.86796265979737 usec\nrounds: 3669"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 253473.03462848772,
            "unit": "iter/sec",
            "range": "stddev: 5.962882162449452e-7",
            "extra": "mean: 3.9451928346764285 usec\nrounds: 32909"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 253006.74276423373,
            "unit": "iter/sec",
            "range": "stddev: 5.992633764165706e-7",
            "extra": "mean: 3.9524638318902734 usec\nrounds: 60274"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 252814.93367079366,
            "unit": "iter/sec",
            "range": "stddev: 6.127019779700419e-7",
            "extra": "mean: 3.9554625412364417 usec\nrounds: 83452"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 251394.60205481172,
            "unit": "iter/sec",
            "range": "stddev: 6.348417871462648e-7",
            "extra": "mean: 3.977810151158175 usec\nrounds: 73606"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 229893.3520469283,
            "unit": "iter/sec",
            "range": "stddev: 0.000004504870676191633",
            "extra": "mean: 4.349843051554919 usec\nrounds: 80039"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 233907.94654537705,
            "unit": "iter/sec",
            "range": "stddev: 0.000003909812792226954",
            "extra": "mean: 4.275186092516975 usec\nrounds: 76075"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24388.001088195528,
            "unit": "iter/sec",
            "range": "stddev: 0.0000031758830097884806",
            "extra": "mean: 41.0037705174627 usec\nrounds: 6933"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "12698fbd4e52dc1a0fcac4b5658dcc4f3c9e5343",
          "message": "Merge pull request #184 from developmentseed/docs/bbox-tiles-example\n\ndocs: add example for finding tiles for a bounding box",
          "timestamp": "2025-09-25T13:51:17-06:00",
          "tree_id": "58049476cd06136890aca33e25cd2ff968e492e4",
          "url": "https://github.com/developmentseed/morecantile/commit/12698fbd4e52dc1a0fcac4b5658dcc4f3c9e5343"
        },
        "date": 1758829955857,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 11320.621836832728,
            "unit": "iter/sec",
            "range": "stddev: 0.0000065919536752859485",
            "extra": "mean: 88.33437017977265 usec\nrounds: 1167"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 11403.887504002123,
            "unit": "iter/sec",
            "range": "stddev: 0.000006326726010802459",
            "extra": "mean: 87.6893953618059 usec\nrounds: 7158"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 11464.549046941029,
            "unit": "iter/sec",
            "range": "stddev: 0.00000591207289322304",
            "extra": "mean: 87.22541077765462 usec\nrounds: 7330"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 11531.382116973615,
            "unit": "iter/sec",
            "range": "stddev: 0.000006433754500344252",
            "extra": "mean: 86.71987363319184 usec\nrounds: 7225"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 11338.027981995569,
            "unit": "iter/sec",
            "range": "stddev: 0.000008295686511781228",
            "extra": "mean: 88.19875921879611 usec\nrounds: 7322"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 11458.485072076612,
            "unit": "iter/sec",
            "range": "stddev: 0.000009490571726847027",
            "extra": "mean: 87.27157156550459 usec\nrounds: 7301"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 7085.967712036837,
            "unit": "iter/sec",
            "range": "stddev: 0.00000830396555806449",
            "extra": "mean: 141.12398484420322 usec\nrounds: 3563"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 248768.36336935157,
            "unit": "iter/sec",
            "range": "stddev: 6.38234805320994e-7",
            "extra": "mean: 4.019803750186993 usec\nrounds: 74823"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 249926.8181840883,
            "unit": "iter/sec",
            "range": "stddev: 6.247206106481114e-7",
            "extra": "mean: 4.001171251911955 usec\nrounds: 81348"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 253320.38555878573,
            "unit": "iter/sec",
            "range": "stddev: 6.164120922423667e-7",
            "extra": "mean: 3.947570179929081 usec\nrounds: 82488"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 254131.63315021788,
            "unit": "iter/sec",
            "range": "stddev: 6.208188898975798e-7",
            "extra": "mean: 3.934968612934925 usec\nrounds: 84589"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 247046.47941032084,
            "unit": "iter/sec",
            "range": "stddev: 6.958504494893894e-7",
            "extra": "mean: 4.0478212941423655 usec\nrounds: 80238"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 246056.91269096223,
            "unit": "iter/sec",
            "range": "stddev: 6.472977669550302e-7",
            "extra": "mean: 4.064100411013286 usec\nrounds: 75908"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24531.54084695401,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033350208432509582",
            "extra": "mean: 40.76384790660903 usec\nrounds: 10796"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "5ef8604641e0bb91f8c39d2c5ada0604efc7b2c4",
          "message": "Merge pull request #186 from developmentseed/patch/json-to-model-dump\n\nupdate deprecated",
          "timestamp": "2025-11-03T09:34:36+01:00",
          "tree_id": "662661f9653680fa6f671966730fedb3ffdb3d8b",
          "url": "https://github.com/developmentseed/morecantile/commit/5ef8604641e0bb91f8c39d2c5ada0604efc7b2c4"
        },
        "date": 1762158955195,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 10994.13674056625,
            "unit": "iter/sec",
            "range": "stddev: 0.000006291987267921458",
            "extra": "mean: 90.95757344095897 usec\nrounds: 994"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 10992.486352927806,
            "unit": "iter/sec",
            "range": "stddev: 0.000006796608716535269",
            "extra": "mean: 90.9712296102741 usec\nrounds: 6903"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 11074.256905126429,
            "unit": "iter/sec",
            "range": "stddev: 0.000006264803395112816",
            "extra": "mean: 90.29951251510934 usec\nrounds: 6552"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 11157.591053360276,
            "unit": "iter/sec",
            "range": "stddev: 0.000009035912563405371",
            "extra": "mean: 89.6250808277146 usec\nrounds: 6718"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 11162.436182039663,
            "unit": "iter/sec",
            "range": "stddev: 0.000008607710216441825",
            "extra": "mean: 89.58617847320802 usec\nrounds: 6550"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 11257.552492488008,
            "unit": "iter/sec",
            "range": "stddev: 0.000006574358880419165",
            "extra": "mean: 88.8292549084079 usec\nrounds: 6214"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 6953.043169997971,
            "unit": "iter/sec",
            "range": "stddev: 0.000010693725781156958",
            "extra": "mean: 143.82191733181656 usec\nrounds: 3508"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 249970.1444143512,
            "unit": "iter/sec",
            "range": "stddev: 6.116185205770731e-7",
            "extra": "mean: 4.000477746423978 usec\nrounds: 70393"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 246270.51689494136,
            "unit": "iter/sec",
            "range": "stddev: 6.623875169768299e-7",
            "extra": "mean: 4.06057538924401 usec\nrounds: 56520"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 247567.9635153055,
            "unit": "iter/sec",
            "range": "stddev: 5.673437368521366e-7",
            "extra": "mean: 4.039294849788496 usec\nrounds: 68696"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 248437.38427818162,
            "unit": "iter/sec",
            "range": "stddev: 6.101320542307926e-7",
            "extra": "mean: 4.025159107617535 usec\nrounds: 68130"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 239417.06047393268,
            "unit": "iter/sec",
            "range": "stddev: 6.611670359256497e-7",
            "extra": "mean: 4.176811786179616 usec\nrounds: 66366"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 243195.977017367,
            "unit": "iter/sec",
            "range": "stddev: 8.841501688596858e-7",
            "extra": "mean: 4.111910123943327 usec\nrounds: 67760"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 24004.567540693468,
            "unit": "iter/sec",
            "range": "stddev: 0.000003700794791288039",
            "extra": "mean: 41.658738417376675 usec\nrounds: 8353"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "vincent.sarago@gmail.com",
            "name": "vincentsarago",
            "username": "vincentsarago"
          },
          "distinct": true,
          "id": "329b722ff376d3a88b531c2e5731fd8652829704",
          "message": "Merge branch 'main' of https://github.com/developmentseed/morecantile",
          "timestamp": "2025-11-06T09:13:55+01:00",
          "tree_id": "a4ec8d5b18ef9ca6eaf0f70342e72bde8abf673d",
          "url": "https://github.com/developmentseed/morecantile/commit/329b722ff376d3a88b531c2e5731fd8652829704"
        },
        "date": 1762416933747,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 10674.727046208409,
            "unit": "iter/sec",
            "range": "stddev: 0.000006832489993840176",
            "extra": "mean: 93.67921031340968 usec\nrounds: 989"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 10675.554176519194,
            "unit": "iter/sec",
            "range": "stddev: 0.000006606579150182303",
            "extra": "mean: 93.6719521502212 usec\nrounds: 6604"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 10754.225532249397,
            "unit": "iter/sec",
            "range": "stddev: 0.000006584834620135454",
            "extra": "mean: 92.986705272382 usec\nrounds: 6847"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 10826.514452341455,
            "unit": "iter/sec",
            "range": "stddev: 0.000007079538620442341",
            "extra": "mean: 92.36583060984411 usec\nrounds: 6854"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 10816.63074576338,
            "unit": "iter/sec",
            "range": "stddev: 0.000006836296289923168",
            "extra": "mean: 92.4502299749556 usec\nrounds: 6005"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 10805.99534424814,
            "unit": "iter/sec",
            "range": "stddev: 0.0000069337123244967065",
            "extra": "mean: 92.54122069673888 usec\nrounds: 5827"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 6835.069393518979,
            "unit": "iter/sec",
            "range": "stddev: 0.000008878524498429516",
            "extra": "mean: 146.30429369864206 usec\nrounds: 3650"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 245919.59377781273,
            "unit": "iter/sec",
            "range": "stddev: 5.971845894879738e-7",
            "extra": "mean: 4.066369761912894 usec\nrounds: 55698"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 246469.98323249596,
            "unit": "iter/sec",
            "range": "stddev: 5.943344242550667e-7",
            "extra": "mean: 4.057289195563813 usec\nrounds: 75793"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 245699.33670264148,
            "unit": "iter/sec",
            "range": "stddev: 6.794589303757486e-7",
            "extra": "mean: 4.070015057510121 usec\nrounds: 75444"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 246591.70177858553,
            "unit": "iter/sec",
            "range": "stddev: 5.72126073186462e-7",
            "extra": "mean: 4.055286503103414 usec\nrounds: 72802"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 234951.7572763956,
            "unit": "iter/sec",
            "range": "stddev: 6.512369349088399e-7",
            "extra": "mean: 4.256192895052949 usec\nrounds: 71246"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 234128.5459234131,
            "unit": "iter/sec",
            "range": "stddev: 6.709989635550051e-7",
            "extra": "mean: 4.271157948963279 usec\nrounds: 72802"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 23596.749568617157,
            "unit": "iter/sec",
            "range": "stddev: 0.000006047132731443705",
            "extra": "mean: 42.37871818286212 usec\nrounds: 8431"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "vincent.sarago@gmail.com",
            "name": "Vincent Sarago",
            "username": "vincentsarago"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "d7e6f21965448d82e8b4385f6f61cd7b60ede883",
          "message": "Merge pull request #190 from developmentseed/feature/switch-to-uv\n\nswitch to UV",
          "timestamp": "2025-11-18T09:36:44+01:00",
          "tree_id": "1357ad19bed02a6fd1e5be319d9654831ab092bb",
          "url": "https://github.com/developmentseed/morecantile/commit/d7e6f21965448d82e8b4385f6f61cd7b60ede883"
        },
        "date": 1763455081907,
        "tool": "pytest",
        "benches": [
          {
            "name": "morecantile.bounds-Tile(x=0,y=0,z=0)",
            "value": 13592.303814204717,
            "unit": "iter/sec",
            "range": "stddev: 0.000005198490735728654",
            "extra": "mean: 73.5710453260281 usec\nrounds: 1059"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=0,z=1)",
            "value": 13662.517646423436,
            "unit": "iter/sec",
            "range": "stddev: 0.000005730863531260246",
            "extra": "mean: 73.1929521248801 usec\nrounds: 7624"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=1,z=1)",
            "value": 13670.562109816341,
            "unit": "iter/sec",
            "range": "stddev: 0.000005503092970142431",
            "extra": "mean: 73.14988161912784 usec\nrounds: 7535"
          },
          {
            "name": "morecantile.bounds-Tile(x=1,y=40,z=7)",
            "value": 13627.496370971074,
            "unit": "iter/sec",
            "range": "stddev: 0.000010183207591411828",
            "extra": "mean: 73.38105054499762 usec\nrounds: 7340"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=10)",
            "value": 13836.384190953604,
            "unit": "iter/sec",
            "range": "stddev: 0.000005432135635789319",
            "extra": "mean: 72.27321720755717 usec\nrounds: 7334"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=20)",
            "value": 13750.46285587093,
            "unit": "iter/sec",
            "range": "stddev: 0.00000545165734016985",
            "extra": "mean: 72.72482464639637 usec\nrounds: 7636"
          },
          {
            "name": "morecantile.bounds-Tile(x=486,y=332,z=30)",
            "value": 8449.360139383769,
            "unit": "iter/sec",
            "range": "stddev: 0.000007298719235435276",
            "extra": "mean: 118.35215726441177 usec\nrounds: 3758"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=0,y=0,z=0)",
            "value": 333420.928356004,
            "unit": "iter/sec",
            "range": "stddev: 5.676078525936229e-7",
            "extra": "mean: 2.9992118519095134 usec\nrounds: 75279"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=0,z=1)",
            "value": 334554.96579387446,
            "unit": "iter/sec",
            "range": "stddev: 5.333099553595984e-7",
            "extra": "mean: 2.9890454551379118 usec\nrounds: 77131"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=1,z=1)",
            "value": 323042.0598157681,
            "unit": "iter/sec",
            "range": "stddev: 7.774704773827055e-7",
            "extra": "mean: 3.095572138718727 usec\nrounds: 74433"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=1,y=40,z=7)",
            "value": 330778.18072072224,
            "unit": "iter/sec",
            "range": "stddev: 5.312703889614165e-7",
            "extra": "mean: 3.0231740129325675 usec\nrounds: 70943"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=10)",
            "value": 330909.72941092175,
            "unit": "iter/sec",
            "range": "stddev: 5.797945321736877e-7",
            "extra": "mean: 3.0219721909663337 usec\nrounds: 67532"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=20)",
            "value": 330852.5316138906,
            "unit": "iter/sec",
            "range": "stddev: 5.759351561020294e-7",
            "extra": "mean: 3.0224946296225217 usec\nrounds: 71969"
          },
          {
            "name": "morecantile.xy_bounds-Tile(x=486,y=332,z=30)",
            "value": 27843.921473447546,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029458076138203046",
            "extra": "mean: 35.9144814049852 usec\nrounds: 9196"
          }
        ]
      }
    ]
  }
}