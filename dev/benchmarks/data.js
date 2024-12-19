window.BENCHMARK_DATA = {
  "lastUpdate": 1734636361022,
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
      }
    ]
  }
}